import random
import spacy
from spacy.util import minibatch, compounding


class SentimentalAnalysis:
    def __init__(self):
        self.error = ''
        self.loaded_model = spacy.load("model_artifacts")

    def train_model(self, training_data, test_data, iterations: int = 200):
        # Build pipeline
        nlp = spacy.load("en_core_web_sm")
        if "textcat" not in nlp.pipe_names:
            textcat = nlp.create_pipe("textcat", config={"architecture": "simple_cnn"})
            nlp.add_pipe(textcat, last=True)
        else:
            textcat = nlp.get_pipe("textcat")

        textcat.add_label("pos")
        textcat.add_label("neg")

        training_excluded_pipes = [
            pipe for pipe in nlp.pipe_names if pipe != "textcat"
        ]
        with nlp.disable_pipes(training_excluded_pipes):
            optimizer = nlp.begin_training()
            # Training loop
            print("Begin training")
            print("Loss\t Precision\t Recall\t F-score")
            batch_sizes = compounding(4.0, 32.0, 1.001)  # Yields an infinite series of compounding value
            for i in range(iterations):
                print(f"Training iteration {i}")
                loss = {}
                random.shuffle(training_data)
                batches = minibatch(training_data, size=batch_sizes)
                for batch in batches:
                    text, labels = zip(*batch)
                    nlp.update(text, labels, drop=0.2, sgd=optimizer, losses=loss)
                with textcat.model.use_params(optimizer.averages):
                    evaluation_results = self.evaluate_model(
                        tokenizer=nlp.tokenizer,
                        textcat=textcat,
                        test_data=test_data,
                    )
                    print(
                        f"{loss['textcat']}\t{evaluation_results['precision']}"
                        f"\t{evaluation_results['recall']}"
                        f"\t{evaluation_results['f-score']}"
                    )

        # Save model
        with nlp.use_params(optimizer.averages):
            nlp.to_disk("model_artifacts")

    @staticmethod
    def evaluate_model(tokenizer, textcat, test_data):
        reviews, labels = zip(*test_data)
        reviews = (tokenizer(review) for review in reviews)
        true_positives = 0
        false_positives = 1e-8  # Can't be 0 because of presence in denominator
        true_negatives = 0
        false_negatives = 1e-8
        for i, review in enumerate(textcat.pipe(reviews)):
            true_label = labels[i]["cats"]
            for predicted_label, score in review.cats.items():
                # uses cats dictionary pos label
                if predicted_label == "neg":
                    continue
                if score >= 0.5 and true_label["pos"]:
                    true_positives += 1
                elif score >= 0.5 and true_label["neg"]:
                    false_positives += 1
                elif score < 0.5 and true_label["neg"]:
                    true_negatives += 1
                elif score < 0.5 and true_label["pos"]:
                    false_negatives += 1
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)

        if precision + recall == 0:
            f_score = 0
        else:
            f_score = 2 * (precision * recall) / (precision + recall)
        return {"precision": precision, "recall": recall, "f-score": f_score}

    def test_model(self, input_data):
        # Generate prediction
        parsed_text = self.loaded_model(input_data)
        # Determine prediction to return
        if parsed_text.cats["pos"] > parsed_text.cats["neg"]:
            prediction = "Positive"
            score = parsed_text.cats["pos"]
        else:
            prediction = "Negative"
            score = parsed_text.cats["neg"]

        print(f"text: {input_data}\n sentiment: {prediction} \t Score: {score}")
        return input_data, prediction, score
        # print(f"text: {input_data}\n sentiment: {prediction} \t Score: {score}")

    @staticmethod
    def load_training_data(data: list, split: float = 0.8, limit: int = 0):
        # Load from files
        reviews = []
        for i in data:
            if i[0].strip():
                spacy_label = {
                    "cats": {
                        "pos": "POS" == i[1],
                        "neg": "NEG" == i[1],
                    }
                }
                reviews.append((i[0], spacy_label))
        random.shuffle(reviews)

        if limit:
            reviews = reviews[:limit]
        split = int(len(reviews) * split)
        return reviews[:split], reviews[split:]

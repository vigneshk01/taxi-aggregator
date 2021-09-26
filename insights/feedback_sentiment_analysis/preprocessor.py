import spacy


class Preprocessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def convert_as_doc(self, cmt_str):
        text_doc = self.nlp(cmt_str)
        return text_doc

    def fetch_entity(self, cmt_str):
        doc = self.convert_as_doc(cmt_str)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_, spacy.explain(ent.label_))

    @staticmethod
    def validate_stopword_punc(token_val):
        # words_aft_stopword_punc = [token for token in text_doc if not token.is_stop and not token.is_punct]
        if not token_val.is_stop and not token_val.is_punct:
            return True
        return False

    @staticmethod
    def perform_lemma(token_val):
        # lemma_tokens = [token.lemma_ for token in words_aft_stopword_punc]
        return token_val.lemma_

    @staticmethod
    def hide_person_names(token_val):
        if token_val.ent_iob != 0 and token_val.ent_type_ == 'PERSON':
            return ''
        return token_val.text

    def redact_names(self, nlp_doc):
        with nlp_doc.retokenize() as retokenizer:
            for ent in nlp_doc.ents:
                retokenizer.merge(ent)
        tokens = map(self.hide_person_names, nlp_doc)
        return ''.join(tokens)

    def data_cleansing(self, cmt_str):
        # sentence_lst = []
        # text_doc = nlp(str(comment_lst[0]))
        """for i in lst:
            text_doc = self.nlp(str(i))
            self.redact_names(text_doc)

            word_lst = []
            for token in text_doc:
                if self.validate_stopword_punc(token):
                    lemma_op = self.perform_lemma(token)
                    word_lst.append(lemma_op)

            sentence_lst.append(word_lst)

        return sentence_lst"""

        text_doc = self.nlp(cmt_str)
        self.redact_names(text_doc)

        word_lst = []
        for token in text_doc:
            if self.validate_stopword_punc(token):
                lemma_op = self.perform_lemma(token)
                word_lst.append(lemma_op)

        return " ".join(word_lst)

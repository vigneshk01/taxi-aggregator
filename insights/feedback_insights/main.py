from collections import Counter
import pandas as pd
from database import Database
from preprocessor import Preprocessor
from sentiment_analysis import SentimentalAnalysis
import numpy as np
import matplotlib.pyplot as plt

eval_list, comment_lst, txt_lst = [], [], []
db = Database()
pre_pros = Preprocessor()

comments = (list(db.get_all_data('reviews', {}, {'_id': 0, 'comment': 1, 'flag': 1})))
for i in comments:
    text_str = pre_pros.data_cleansing(i['comment'])
    comment_lst.append((text_str, i['flag']))
    txt_lst.append(text_str)

sa = SentimentalAnalysis()
train, test = sa.load_training_data(data=comment_lst, limit=25)
# print(f"Training model {train}")
# sa.train_model(train, test)
df = pd.DataFrame(eval_list)
pd.DataFrame.plot(df)
print("Testing model")

positive_count, negative_count, total_score = 0, 0, 0
for i in comment_lst:
    TEST_REVIEW = str(i[0])
    op_data = sa.test_model(TEST_REVIEW)
    if op_data[1] == 'Positive':
        positive_count += 1
    elif op_data[1] == 'Negative':
        negative_count += 1
    total_score += op_data[2]
print("total_pos_feedback %s, total_neg_feedback %s" % (positive_count, negative_count))
# print("avg_score %s" % (total_score / (positive_count + negative_count)))


# Word Bubble
comments = [i['comment'] for i in comments]
lemmanted_words = pre_pros.data_cleansing(' '.join(comments))
word_freq = Counter(lemmanted_words.split())

# Common words
common_words = word_freq.most_common(5)
print(common_words)

# Unique words
unique_words = [word for (word, freq) in word_freq.items() if freq == 1]
print(unique_words)

# displacy.serve(pre_pros.covert_as_doc(' , '.join(txt_lst)), style='dep')
# displacy.serve(pre_pros.covert_as_doc(' , '.join(txt_lst)), style='ent')


polarities = ['positive', 'negative']
values = [positive_count, negative_count]

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(polarities, values, color='maroon', width=0.4)

plt.xlabel("Polarities")
plt.ylabel("Total Count")
plt.title("Sentimental Analysis of the customers feedback")
plt.show()

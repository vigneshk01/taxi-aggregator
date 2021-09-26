some of the Dataset used for training the model:
Kaggle - uber-reviews-text-analysis
Kaggle - NLP Classification Dataset

Notes:
The sentimental analysis SPACY library is used for NLP Training and classification

steps to install:
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm

The setup uses 'textcat' spacy pipeline to perform word classification and architecture as 'simple cnn'
The accuracy and optimization of the feedback score is a work in progress.


Word visualization:
pip3 install nltk

This is a simple word collater uses nltk to tokenize the words and performs basic preprocessing to streamline the word collection.
Display most frequently used words during the feedback.

This helps mine interesting keywords (requests/issues) reported by user that may not be considered normally.
The optimized way of finding unique words/most frequented words is still a work in progress
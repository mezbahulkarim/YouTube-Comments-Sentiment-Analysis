# Takes too long not ideal, 70 seconds per inference

from flair.data import Sentence
from flair.nn import Classifier

# make a sentence
sentence = Sentence('I love Berlin and New York.')

# load the sentiment tagger
tagger = Classifier.load('sentiment')

# run sentiment analysis over sentence
tagger.predict(sentence)

# print the sentence with all annotations
print(sentence)
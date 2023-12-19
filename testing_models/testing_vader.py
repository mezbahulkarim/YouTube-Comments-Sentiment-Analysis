# Same results as BERT and fast plus compund score is better

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentence = "I love winter"

analzyer = SentimentIntensityAnalyzer()

sentiment_dict = analzyer.polarity_scores(sentence)

print(sentiment_dict)
print(f"The sentence had a score of: {sentiment_dict['compound']}")

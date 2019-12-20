from sentiment_analyzer import SentimentAnalyzer

sa = SentimentAnalyzer()
sa.create_model(False)
res = sa.predict("It was awful movie")
print(res)
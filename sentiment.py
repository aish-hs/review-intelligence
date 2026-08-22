from textblob import TextBlob


# ==================================================
# SENTIMENT ANALYSIS
# ==================================================

def analyze_sentiment(review):

    analysis = TextBlob(review)

    polarity = analysis.sentiment.polarity

    if polarity > 0.1:

        sentiment = "Positive"

    elif polarity < -0.1:

        sentiment = "Negative"

    else:

        sentiment = "Neutral"

    return sentiment, polarity
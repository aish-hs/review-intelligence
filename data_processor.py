from sentiment import analyze_sentiment
from topics import detect_aspects


# ==================================================
# ANALYZE MULTIPLE REVIEWS
# ==================================================

def analyze_reviews(
    data,
    review_column
):

    sentiments = []

    scores = []

    topics = []

    for review_text in data[
        review_column
    ].fillna(""):

        sentiment, polarity = analyze_sentiment(
            str(review_text)
        )

        aspects = detect_aspects(
            str(review_text)
        )

        sentiments.append(
            sentiment
        )

        scores.append(
            polarity
        )

        topics.append(
            ", ".join(aspects)
        )

    data["Sentiment"] = sentiments

    data["Sentiment Score"] = scores

    data["Topics"] = topics

    return data


# ==================================================
# COUNT TOPICS
# ==================================================

def get_topic_counts(data):

    topic_counts = {}

    for topic_list in data["Topics"]:

        if topic_list:

            for topic in topic_list.split(", "):

                topic_counts[topic] = (
                    topic_counts.get(topic, 0) + 1
                )

    return topic_counts


# ==================================================
# DETECT CUSTOMER PROBLEMS
# ==================================================

def get_problem_counts(data):

    problem_counts = {}

    negative_reviews = data[
        data["Sentiment"] == "Negative"
    ]

    for topic_list in negative_reviews[
        "Topics"
    ]:

        if topic_list:

            for topic in topic_list.split(", "):

                problem_counts[topic] = (
                    problem_counts.get(topic, 0) + 1
                )

    return problem_counts
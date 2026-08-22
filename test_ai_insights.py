from ai_insights import generate_ai_insights


# Sample statistics similar to our dashboard
total_reviews = 6

positive_count = 3
neutral_count = 1
negative_count = 2

positive_percent = 50.0
negative_percent = 33.3

topic_counts = {
    "Delivery": 3,
    "Product Quality": 2,
    "Packaging": 1
}

problem_counts = {
    "Delivery": 2,
    "Product Quality": 1
}


print("🚀 Testing AI Insights...\n")


try:

    insights = generate_ai_insights(
        total_reviews,
        positive_count,
        neutral_count,
        negative_count,
        positive_percent,
        negative_percent,
        topic_counts,
        problem_counts
    )

    print("✅ AI Insights working!\n")

    for insight in insights:

        print(insight)


except Exception as error:

    print("❌ AI Insights failed!")
    print(type(error).__name__)
    print(error)
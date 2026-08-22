# ==================================================
# ADVANCED TREND & PATTERN INTELLIGENCE
# ==================================================

import pandas as pd


# ==================================================
# SENTIMENT TREND ANALYSIS
# ==================================================

def analyze_sentiment_trend(data):
    """
    Analyze whether customer sentiment is improving,
    worsening, or stable across the review sequence.
    """

    if data is None or data.empty:
        return {
            "trend": "NO DATA",
            "direction": "No trend available",
            "first_half_average": 0,
            "second_half_average": 0,
            "change": 0
        }

    if "Sentiment Score" not in data.columns:
        return {
            "trend": "NO DATA",
            "direction": "Sentiment score unavailable",
            "first_half_average": 0,
            "second_half_average": 0,
            "change": 0
        }

    if len(data) < 2:
        return {
            "trend": "INSUFFICIENT DATA",
            "direction": "At least two reviews are required",
            "first_half_average": 0,
            "second_half_average": 0,
            "change": 0
        }

    scores = pd.to_numeric(
        data["Sentiment Score"],
        errors="coerce"
    ).dropna()

    if len(scores) < 2:
        return {
            "trend": "INSUFFICIENT DATA",
            "direction": "At least two valid sentiment scores are required",
            "first_half_average": 0,
            "second_half_average": 0,
            "change": 0
        }

    midpoint = len(scores) // 2

    first_half = scores.iloc[:midpoint]
    second_half = scores.iloc[midpoint:]

    first_average = round(
        first_half.mean(),
        2
    )

    second_average = round(
        second_half.mean(),
        2
    )

    change = round(
        second_average - first_average,
        2
    )

    threshold = 0.10

    if change > threshold:

        trend = "IMPROVING"

        direction = (
            "Customer sentiment is improving "
            "across the review sequence."
        )

    elif change < -threshold:

        trend = "WORSENING"

        direction = (
            "Customer sentiment is worsening "
            "across the review sequence."
        )

    else:

        trend = "STABLE"

        direction = (
            "Customer sentiment is relatively stable "
            "across the review sequence."
        )

    return {
        "trend": trend,
        "direction": direction,
        "first_half_average": first_average,
        "second_half_average": second_average,
        "change": change
    }


# ==================================================
# RECURRING PROBLEM ANALYSIS
# ==================================================

def analyze_recurring_problems(
    problem_counts,
    total_reviews
):
    """
    Identify problems that repeatedly appear
    across customer reviews.
    """

    recurring_problems = []

    if not problem_counts:
        return recurring_problems

    if total_reviews <= 0:
        return recurring_problems

    for problem, count in problem_counts.items():

        percentage = round(
            (count / total_reviews) * 100,
            1
        )

        if count >= 3:

            recurrence = "HIGHLY RECURRING"

        elif count >= 2:

            recurrence = "RECURRING"

        else:

            recurrence = "OCCASIONAL"

        recurring_problems.append(
            {
                "problem": problem,
                "count": int(count),
                "percentage": percentage,
                "recurrence": recurrence
            }
        )

    recurring_problems = sorted(
        recurring_problems,
        key=lambda item: item["count"],
        reverse=True
    )

    return recurring_problems


# ==================================================
# TOPIC-PROBLEM RELATIONSHIP ANALYSIS
# ==================================================

def analyze_topic_problem_relationships(data):
    """
    Identify which topics commonly appear together
    with customer problems.
    """

    relationships = []

    if data is None or data.empty:
        return relationships

    required_columns = [
        "Topics",
        "Problems"
    ]

    for column in required_columns:

        if column not in data.columns:
            return relationships

    relationship_counts = {}

    for _, row in data.iterrows():

        topics = row.get(
            "Topics",
            ""
        )

        problems = row.get(
            "Problems",
            ""
        )

        if not topics or not problems:
            continue

        topic_list = [
            topic.strip()
            for topic in str(topics).split(",")
            if topic.strip()
        ]

        problem_list = [
            problem.strip()
            for problem in str(problems).split(",")
            if problem.strip()
        ]

        for topic in topic_list:

            for problem in problem_list:

                key = (
                    topic,
                    problem
                )

                relationship_counts[key] = (
                    relationship_counts.get(
                        key,
                        0
                    )
                    + 1
                )

    for key, count in relationship_counts.items():

        topic = key[0]
        problem = key[1]

        relationships.append(
            {
                "topic": topic,
                "problem": problem,
                "count": int(count)
            }
        )

    relationships = sorted(
        relationships,
        key=lambda item: item["count"],
        reverse=True
    )

    return relationships


# ==================================================
# PATTERN ALERT GENERATION
# ==================================================

def generate_pattern_alerts(
    sentiment_trend,
    recurring_problems,
    topic_problem_relationships
):
    """
    Generate important business alerts based on
    detected customer patterns.
    """

    alerts = []

    # ==================================================
    # SENTIMENT ALERT
    # ==================================================

    trend = sentiment_trend.get(
        "trend",
        ""
    )

    if trend == "WORSENING":

        alerts.append(
            {
                "level": "HIGH",
                "title": "Worsening Customer Sentiment",
                "message": (
                    "Customer sentiment is declining "
                    "across the review sequence."
                )
            }
        )

    elif trend == "IMPROVING":

        alerts.append(
            {
                "level": "POSITIVE",
                "title": "Improving Customer Sentiment",
                "message": (
                    "Customer sentiment is improving "
                    "across the review sequence."
                )
            }
        )

    # ==================================================
    # RECURRING PROBLEM ALERTS
    # ==================================================

    for item in recurring_problems:

        problem = item.get(
            "problem",
            "Unknown"
        )

        count = item.get(
            "count",
            0
        )

        recurrence = item.get(
            "recurrence",
            "OCCASIONAL"
        )

        if recurrence == "HIGHLY RECURRING":

            alerts.append(
                {
                    "level": "CRITICAL",
                    "title": f"Highly Recurring Problem: {problem}",
                    "message": (
                        f"{problem} appears in "
                        f"{count} customer review(s) "
                        "and requires immediate attention."
                    )
                }
            )

        elif recurrence == "RECURRING":

            alerts.append(
                {
                    "level": "HIGH",
                    "title": f"Recurring Problem: {problem}",
                    "message": (
                        f"{problem} repeatedly appears in "
                        f"{count} customer review(s)."
                    )
                }
            )

    # ==================================================
    # TOPIC-PROBLEM RELATIONSHIP ALERT
    # ==================================================

    if topic_problem_relationships:

        strongest_relationship = (
            topic_problem_relationships[0]
        )

        count = strongest_relationship.get(
            "count",
            0
        )

        if count >= 2:

            topic = strongest_relationship.get(
                "topic",
                "Unknown"
            )

            problem = strongest_relationship.get(
                "problem",
                "Unknown"
            )

            alerts.append(
                {
                    "level": "MEDIUM",
                    "title": "Strong Topic–Problem Relationship",
                    "message": (
                        f"The topic '{topic}' is strongly "
                        f"associated with the problem "
                        f"'{problem}' in {count} review(s)."
                    )
                }
            )

    return alerts


# ==================================================
# COMPLETE TREND INTELLIGENCE
# ==================================================

def generate_trend_intelligence(
    data,
    problem_counts,
    total_reviews
):
    """
    Generate complete advanced trend and
    pattern intelligence.
    """

    sentiment_trend = analyze_sentiment_trend(
        data
    )

    recurring_problems = analyze_recurring_problems(
        problem_counts=problem_counts,
        total_reviews=total_reviews
    )

    topic_problem_relationships = (
        analyze_topic_problem_relationships(
            data
        )
    )

    pattern_alerts = generate_pattern_alerts(
        sentiment_trend=sentiment_trend,
        recurring_problems=recurring_problems,
        topic_problem_relationships=
            topic_problem_relationships
    )

    return {
        "sentiment_trend": sentiment_trend,
        "recurring_problems": recurring_problems,
        "topic_problem_relationships":
            topic_problem_relationships,
        "pattern_alerts": pattern_alerts
    }
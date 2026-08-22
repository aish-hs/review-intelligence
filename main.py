# ============================================================
# REVIEW INTELLIGENCE - MAIN ENGINE
# ============================================================

import re
from collections import Counter, defaultdict

import pandas as pd


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS = {
    "Product Quality": [
        "quality",
        "defect",
        "defective",
        "broken",
        "damaged",
        "faulty",
        "poor quality",
        "bad quality",
        "product issue",
        "product problem",
        "not working",
        "stopped working",
        "works poorly",
        "reliability",
        "durable",
        "durability",
        "material",
        "performance"
    ],

    "Delivery": [
        "delivery",
        "delivered",
        "shipping",
        "shipment",
        "late",
        "delay",
        "delayed",
        "arrived late",
        "delivery time",
        "courier",
        "package arrived",
        "delivery partner"
    ],

    "Packaging": [
        "packaging",
        "package",
        "box",
        "packed",
        "packing",
        "wrapped",
        "damaged package",
        "damaged box",
        "seal",
        "sealed"
    ],

    "Price": [
        "price",
        "expensive",
        "cost",
        "cheap",
        "value",
        "worth",
        "overpriced",
        "money",
        "costly"
    ],

    "Customer Service": [
        "customer service",
        "support",
        "staff",
        "representative",
        "agent",
        "response",
        "help",
        "refund",
        "complaint",
        "service"
    ]
}


# ============================================================
# PROBLEM KEYWORDS
# ============================================================

PROBLEM_KEYWORDS = {
    "Product Quality": [
        "defect",
        "defective",
        "broken",
        "damaged",
        "faulty",
        "poor quality",
        "bad quality",
        "quality issue",
        "quality problem",
        "not working",
        "stopped working",
        "malfunction",
        "malfunctioning",
        "failure",
        "failed",
        "unreliable",
        "poor performance",
        "doesn't work",
        "does not work"
    ],

    "Delivery": [
        "late",
        "delay",
        "delayed",
        "slow delivery",
        "late delivery",
        "not delivered",
        "delivery problem",
        "delivery issue",
        "missing delivery",
        "lost package",
        "shipping problem",
        "shipping issue"
    ],

    "Packaging": [
        "damaged package",
        "damaged box",
        "broken packaging",
        "poor packaging",
        "bad packaging",
        "packaging problem",
        "packaging issue",
        "opened package",
        "torn package",
        "poorly packed",
        "badly packed"
    ],

    "Price": [
        "too expensive",
        "expensive",
        "overpriced",
        "high price",
        "costly",
        "not worth",
        "poor value",
        "bad value",
        "too costly"
    ],

    "Customer Service": [
        "bad support",
        "poor support",
        "bad customer service",
        "poor customer service",
        "rude staff",
        "unhelpful",
        "no response",
        "slow response",
        "support problem",
        "service problem",
        "service issue"
    ]
}


# ============================================================
# ROOT CAUSE KEYWORDS
# ============================================================

ROOT_CAUSE_KEYWORDS = {

    "Product Quality": {
        "Manufacturing / Defect Issue": [
            "defect",
            "defective",
            "faulty",
            "manufacturing",
            "manufactured",
            "malfunction",
            "malfunctioning",
            "broken",
            "failure",
            "failed"
        ],

        "Material / Durability Issue": [
            "material",
            "durability",
            "durable",
            "wear",
            "wearing",
            "fragile",
            "weak",
            "cheap material",
            "poor material"
        ],

        "Performance / Reliability Issue": [
            "performance",
            "reliability",
            "unreliable",
            "not working",
            "doesn't work",
            "does not work",
            "stopped working",
            "works poorly",
            "slow performance"
        ],

        "Quality Control Issue": [
            "quality control",
            "inspection",
            "inspection failed",
            "quality check",
            "qa",
            "quality assurance",
            "inconsistent quality",
            "inconsistent"
        ]
    },

    "Delivery": {
        "Logistics Delay": [
            "late",
            "delay",
            "delayed",
            "slow delivery",
            "late delivery",
            "shipping delay"
        ],

        "Courier / Delivery Partner Issue": [
            "courier",
            "delivery partner",
            "delivery person",
            "driver",
            "shipping company"
        ],

        "Order Fulfillment Issue": [
            "not delivered",
            "missing delivery",
            "lost package",
            "order missing",
            "wrong delivery"
        ]
    },

    "Packaging": {
        "Poor Packaging Process": [
            "poor packaging",
            "bad packaging",
            "poorly packed",
            "badly packed",
            "weak packaging",
            "packaging issue"
        ],

        "Insufficient Protection": [
            "not protected",
            "no protection",
            "damaged box",
            "damaged package",
            "broken packaging",
            "torn package"
        ],

        "Packaging Damage During Transit": [
            "damaged during delivery",
            "damaged during shipping",
            "damaged in transit",
            "arrived damaged",
            "package damaged"
        ]
    },

    "Price": {
        "High Pricing": [
            "too expensive",
            "expensive",
            "overpriced",
            "high price",
            "costly"
        ],

        "Poor Value Perception": [
            "not worth",
            "poor value",
            "bad value",
            "not worth the price",
            "value for money"
        ]
    },

    "Customer Service": {
        "Slow Support Response": [
            "slow response",
            "no response",
            "didn't respond",
            "did not respond",
            "long wait",
            "waiting"
        ],

        "Poor Support Quality": [
            "poor support",
            "bad support",
            "unhelpful",
            "not helpful",
            "bad customer service",
            "poor customer service"
        ],

        "Staff Behaviour": [
            "rude",
            "rude staff",
            "unprofessional",
            "unfriendly"
        ]
    }
}


# ============================================================
# SENTIMENT KEYWORDS
# ============================================================

POSITIVE_WORDS = [
    "good",
    "great",
    "excellent",
    "amazing",
    "awesome",
    "love",
    "loved",
    "perfect",
    "happy",
    "satisfied",
    "satisfaction",
    "best",
    "fantastic",
    "wonderful",
    "nice",
    "easy",
    "fast",
    "quick",
    "reliable",
    "worth",
    "recommend",
    "recommended"
]


NEGATIVE_WORDS = [
    "bad",
    "poor",
    "terrible",
    "worst",
    "awful",
    "hate",
    "hated",
    "disappointed",
    "disappointing",
    "dissatisfied",
    "problem",
    "issue",
    "broken",
    "defective",
    "defect",
    "damaged",
    "late",
    "delay",
    "delayed",
    "expensive",
    "overpriced",
    "rude",
    "slow",
    "failed",
    "failure",
    "unreliable",
    "not working",
    "doesn't work",
    "does not work"
]


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def analyze_sentiment(text):
    """
    Returns:
        sentiment: Positive / Neutral / Negative
        polarity: float from -1 to +1
    """

    if text is None:
        return "Neutral", 0.0

    text = str(text).lower().strip()

    if not text:
        return "Neutral", 0.0

    positive_score = 0
    negative_score = 0

    for phrase in POSITIVE_WORDS:
        if phrase in text:
            positive_score += 1

    for phrase in NEGATIVE_WORDS:
        if phrase in text:
            negative_score += 1

    total = positive_score + negative_score

    if total == 0:
        return "Neutral", 0.0

    polarity = (
        positive_score - negative_score
    ) / max(1, total)

    if polarity > 0.10:
        sentiment = "Positive"

    elif polarity < -0.10:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, round(polarity, 2)


# ============================================================
# TOPIC DETECTION
# ============================================================

def detect_aspects(text):
    """
    Detects customer topics mentioned in a review.
    """

    if text is None:
        return []

    text = str(text).lower()

    detected = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                detected.append(topic)
                break

    return detected


# ============================================================
# PROBLEM DETECTION
# ============================================================

def detect_problems(text):
    """
    Detects problems from a review.
    """

    if text is None:
        return []

    text = str(text).lower()

    detected = []

    for problem, keywords in PROBLEM_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                detected.append(problem)
                break

    return detected


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(aspects, sentiment):

    recommendations = []

    if not aspects:
        if sentiment == "Negative":
            return [
                "Investigate the negative customer feedback.",
                "Review the customer experience for possible service issues."
            ]

        return [
            "Continue monitoring customer feedback."
        ]

    for aspect in aspects:

        if aspect == "Product Quality":
            recommendations.append(
                "Investigate product defects, quality-control procedures "
                "and product reliability."
            )

        elif aspect == "Delivery":
            recommendations.append(
                "Review delivery timelines, fulfillment operations "
                "and delivery partner performance."
            )

        elif aspect == "Packaging":
            recommendations.append(
                "Improve packaging standards and product protection "
                "during transportation."
            )

        elif aspect == "Price":
            recommendations.append(
                "Review pricing and ensure customer-perceived value "
                "matches the product quality."
            )

        elif aspect == "Customer Service":
            recommendations.append(
                "Improve customer support response time and service quality."
            )

    # Remove duplicates while preserving order
    return list(dict.fromkeys(recommendations))


# ============================================================
# ANALYZE COMPLETE DATASET
# ============================================================

def analyze_reviews(data, review_column):

    data = data.copy()

    sentiments = []
    scores = []
    topics = []
    problems = []

    for review in data[review_column]:

        sentiment, score = analyze_sentiment(review)

        sentiments.append(sentiment)
        scores.append(score)

        detected_topics = detect_aspects(review)
        detected_problems = detect_problems(review)

        topics.append(detected_topics)
        problems.append(detected_problems)

    data["Sentiment"] = sentiments
    data["Sentiment Score"] = scores
    data["Topics"] = topics
    data["Problems"] = problems

    return data


# ============================================================
# TOPIC COUNTS
# ============================================================

def get_topic_counts(data):

    counter = Counter()

    if "Topics" not in data.columns:
        return {}

    for topics in data["Topics"]:

        if isinstance(topics, list):

            for topic in topics:
                counter[topic] += 1

    return dict(counter)


# ============================================================
# PROBLEM COUNTS
# ============================================================

def get_problem_counts(data):

    counter = Counter()

    if "Problems" not in data.columns:
        return {}

    for problems in data["Problems"]:

        if isinstance(problems, list):

            for problem in problems:
                counter[problem] += 1

    return dict(counter)


# ============================================================
# PRIORITY RECOMMENDATION
# ============================================================

def get_priority_recommendation(problem_counts):

    if not problem_counts:

        return None, 0, ""

    priority_problem = max(
        problem_counts,
        key=problem_counts.get
    )

    priority_count = problem_counts[
        priority_problem
    ]

    recommendations = {
        "Product Quality":
            "Investigate product defects, quality-control procedures "
            "and product reliability.",

        "Delivery":
            "Review fulfillment operations and delivery partner performance.",

        "Packaging":
            "Improve packaging standards and product protection.",

        "Price":
            "Review pricing strategy and customer-perceived value.",

        "Customer Service":
            "Improve support response time and customer service quality."
    }

    recommendation = recommendations.get(
        priority_problem,
        "Investigate the main customer problem and improve the related process."
    )

    return (
        priority_problem,
        priority_count,
        recommendation
    )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

def generate_executive_summary(
    positive_percent,
    negative_percent,
    topic_counts
):

    if topic_counts:

        main_topic = max(
            topic_counts,
            key=topic_counts.get
        )

    else:

        main_topic = "customer experience"

    if positive_percent >= 70:

        return (
            f"Customers are generally satisfied with the product. "
            f"The most frequently mentioned topic is {main_topic}."
        )

    elif positive_percent >= 50:

        return (
            f"Customers show mixed but generally positive sentiment. "
            f"The most frequently mentioned topic is {main_topic}. "
            f"However, negative feedback should be investigated."
        )

    else:

        return (
            f"Customer sentiment indicates significant dissatisfaction. "
            f"The most frequently mentioned topic is {main_topic}. "
            f"Immediate investigation of customer problems is recommended."
        )


# ============================================================
# BUSINESS INSIGHT
# ============================================================

def generate_business_insight(negative_percent):

    if negative_percent >= 40:

        return (
            "Customer dissatisfaction is critically high. "
            "Immediate corrective action is recommended."
        )

    elif negative_percent >= 30:

        return (
            "A noticeable number of customers are dissatisfied. "
            "The business should investigate the main problem areas."
        )

    elif negative_percent >= 20:

        return (
            "Some customer experience issues require attention "
            "before they become larger operational problems."
        )

    else:

        return (
            "Customer experience is generally healthy. "
            "Continue monitoring customer feedback."
        )


# ============================================================
# CUSTOMER SATISFACTION
# ============================================================

def calculate_satisfaction(
    positive_count,
    neutral_count,
    negative_count,
    total_reviews
):

    if total_reviews <= 0:
        return 0, "No reviews available."

    score = (
        (
            positive_count
            + (neutral_count * 0.5)
        )
        / total_reviews
    ) * 100

    score = round(score)

    if score >= 80:
        message = "Excellent customer satisfaction."

    elif score >= 60:
        message = "Moderate customer satisfaction."

    elif score >= 40:
        message = "Customer satisfaction needs improvement."

    else:
        message = "Customer satisfaction is critically low."

    return score, message


# ============================================================
# TOPIC SENTIMENT ANALYSIS
# ============================================================

def get_topic_sentiment_analysis(data):

    result = {}

    if "Topics" not in data.columns:
        return result

    for _, row in data.iterrows():

        topics = row.get("Topics", [])

        if not isinstance(topics, list):
            continue

        sentiment = row.get(
            "Sentiment",
            "Neutral"
        )

        for topic in topics:

            if topic not in result:

                result[topic] = {
                    "mentions": 0,
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0,
                    "positive_percent": 0,
                    "neutral_percent": 0,
                    "negative_percent": 0
                }

            result[topic]["mentions"] += 1

            if sentiment == "Positive":
                result[topic]["positive"] += 1

            elif sentiment == "Negative":
                result[topic]["negative"] += 1

            else:
                result[topic]["neutral"] += 1

    for topic, values in result.items():

        total = values["mentions"]

        values["positive_percent"] = round(
            values["positive"] / max(1, total) * 100,
            1
        )

        values["neutral_percent"] = round(
            values["neutral"] / max(1, total) * 100,
            1
        )

        values["negative_percent"] = round(
            values["negative"] / max(1, total) * 100,
            1
        )

    return result


# ============================================================
# PROBLEM SEVERITY ANALYSIS
# ============================================================

def get_problem_severity_analysis(
    problem_counts,
    total_reviews,
    negative_count
):

    result = {}

    if not problem_counts:
        return result

    total_problem_detections = sum(
        problem_counts.values()
    )

    for problem, count in problem_counts.items():

        negative_share = (
            count
            / max(1, total_problem_detections)
        ) * 100

        review_frequency = (
            count
            / max(1, total_reviews)
        ) * 100

        severity_score = (
            negative_share * 0.60
            + review_frequency * 0.40
        )

        severity_score = min(
            100,
            round(severity_score, 1)
        )

        if severity_score >= 70:
            priority = "CRITICAL"

        elif severity_score >= 45:
            priority = "HIGH"

        elif severity_score >= 20:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        result[problem] = {
            "negative_reviews": count,
            "negative_share": round(
                negative_share,
                1
            ),
            "review_frequency": round(
                review_frequency,
                1
            ),
            "severity_score": severity_score,
            "priority": priority
        }

    return result


# ============================================================
# HIGHEST SEVERITY PROBLEM
# ============================================================

def get_highest_severity_problem(problem_severity):

    if not problem_severity:
        return None

    problem = max(
        problem_severity,
        key=lambda x: problem_severity[x]["severity_score"]
    )

    values = problem_severity[problem]

    return {
        "problem": problem,
        **values
    }


# ============================================================
# ROOT CAUSE MATCHING
# ============================================================

def _find_root_cause_matches(
    review_text,
    problem
):

    text = str(review_text).lower()

    causes = ROOT_CAUSE_KEYWORDS.get(
        problem,
        {}
    )

    matches = []

    for cause, keywords in causes.items():

        matched_keywords = []

        for keyword in keywords:

            if keyword.lower() in text:
                matched_keywords.append(keyword)

        if matched_keywords:

            matches.append({
                "cause": cause,
                "matched_keywords": matched_keywords,
                "evidence_count": len(
                    matched_keywords
                )
            })

    return matches


# ============================================================
# ROOT CAUSE INTELLIGENCE
# ============================================================

def generate_root_cause_intelligence(
    data,
    problem_severity
):

    root_cause_analysis = []

    if not problem_severity:

        return {
            "root_cause_analysis": [],
            "highest_priority_root_cause": None
        }

    # --------------------------------------------------------
    # Determine review column
    # --------------------------------------------------------

    review_column = None

    for column in data.columns:

        if str(column).lower().strip() in [
            "review",
            "reviews",
            "text",
            "comment",
            "feedback"
        ]:

            review_column = column
            break

    if review_column is None:
        review_column = data.columns[0]

    # --------------------------------------------------------
    # Analyze each problem
    # --------------------------------------------------------

    for problem, severity in problem_severity.items():

        cause_counter = Counter()
        cause_evidence = defaultdict(list)

        negative_reviews = []

        for _, row in data.iterrows():

            review_text = str(
                row.get(
                    review_column,
                    ""
                )
            )

            sentiment = row.get(
                "Sentiment",
                "Neutral"
            )

            problems = row.get(
                "Problems",
                []
            )

            if not isinstance(problems, list):
                problems = []

            # ------------------------------------------------
            # Only use reviews connected to this problem
            # ------------------------------------------------

            problem_match = (
                problem in problems
            )

            if not problem_match:

                # Also check direct keyword evidence
                for keyword in PROBLEM_KEYWORDS.get(
                    problem,
                    []
                ):

                    if keyword.lower() in review_text.lower():

                        problem_match = True
                        break

            if not problem_match:
                continue

            if sentiment == "Negative":

                negative_reviews.append(
                    review_text
                )

            # ------------------------------------------------
            # Find root cause evidence
            # ------------------------------------------------

            matches = _find_root_cause_matches(
                review_text,
                problem
            )

            for match in matches:

                cause = match["cause"]

                cause_counter[cause] += 1

                cause_evidence[cause].append(
                    review_text
                )

        # ----------------------------------------------------
        # Build root causes
        # ----------------------------------------------------

        root_causes = []

        for cause, count in cause_counter.most_common():

            examples = list(
                dict.fromkeys(
                    cause_evidence[cause]
                )
            )

            root_causes.append({
                "cause": cause,
                "evidence_count": count,
                "example_reviews": examples[:3]
            })

        # ----------------------------------------------------
        # If no exact cause found, derive generic evidence
        # ----------------------------------------------------

        if not root_causes and negative_reviews:

            root_causes.append({
                "cause": (
                    "Specific root cause could not be "
                    "determined from the available review wording"
                ),
                "evidence_count": 0,
                "example_reviews": list(
                    dict.fromkeys(
                        negative_reviews
                    )
                )[:3]
            })

        root_cause_analysis.append({
            "problem": problem,
            "priority": severity.get(
                "priority",
                "LOW"
            ),
            "severity_score": severity.get(
                "severity_score",
                0
            ),
            "negative_reviews": severity.get(
                "negative_reviews",
                0
            ),
            "root_causes": root_causes,
            "example_reviews": list(
                dict.fromkeys(
                    negative_reviews
                )
            )[:3]
        })

    # --------------------------------------------------------
    # Highest priority root cause
    # --------------------------------------------------------

    highest_priority = None

    if root_cause_analysis:

        ordered = sorted(
            root_cause_analysis,
            key=lambda x: (
                x.get("severity_score", 0),
                x.get("negative_reviews", 0)
            ),
            reverse=True
        )

        top = ordered[0]

        if top.get("root_causes"):

            root_cause = top[
                "root_causes"
            ][0]

            highest_priority = {
                "problem": top["problem"],
                "priority": top["priority"],
                "severity_score": top["severity_score"],
                "root_cause": root_cause
            }

    return {
        "root_cause_analysis": root_cause_analysis,
        "highest_priority_root_cause": highest_priority
    }


# ============================================================
# ADVANCED TREND INTELLIGENCE
# ============================================================

def generate_advanced_trend_intelligence(
    data,
    problem_counts,
    total_reviews
):

    sentiment_scores = []

    if "Sentiment Score" in data.columns:

        for value in data["Sentiment Score"]:

            try:
                sentiment_scores.append(
                    float(value)
                )
            except Exception:
                sentiment_scores.append(0.0)

    if not sentiment_scores:

        sentiment_trend = {
            "trend": "NO DATA",
            "direction": "No trend available.",
            "first_half_average": 0,
            "second_half_average": 0,
            "change": 0
        }

    elif len(sentiment_scores) < 2:

        average = sum(
            sentiment_scores
        ) / len(sentiment_scores)

        sentiment_trend = {
            "trend": "STABLE",
            "direction": "Not enough data for a strong trend.",
            "first_half_average": average,
            "second_half_average": average,
            "change": 0
        }

    else:

        midpoint = len(
            sentiment_scores
        ) // 2

        first_half = sentiment_scores[
            :midpoint
        ]

        second_half = sentiment_scores[
            midpoint:
        ]

        first_average = sum(
            first_half
        ) / max(1, len(first_half))

        second_average = sum(
            second_half
        ) / max(1, len(second_half))

        change = (
            second_average
            - first_average
        )

        if change <= -0.15:
            trend = "WORSENING"
            direction = (
                "Customer sentiment is moving downward."
            )

        elif change >= 0.15:
            trend = "IMPROVING"
            direction = (
                "Customer sentiment is improving."
            )

        else:
            trend = "STABLE"
            direction = (
                "Customer sentiment is relatively stable."
            )

        sentiment_trend = {
            "trend": trend,
            "direction": direction,
            "first_half_average": round(
                first_average,
                2
            ),
            "second_half_average": round(
                second_average,
                2
            ),
            "change": round(
                change,
                2
            )
        }

    # --------------------------------------------------------
    # Recurring problems
    # --------------------------------------------------------

    recurring_problems = []

    for problem, count in problem_counts.items():

        percentage = (
            count
            / max(1, total_reviews)
        ) * 100

        if count >= 2:

            if percentage >= 50:
                recurrence = "FREQUENT"

            elif percentage >= 25:
                recurrence = "RECURRING"

            else:
                recurrence = "OCCASIONAL"

            recurring_problems.append({
                "problem": problem,
                "count": count,
                "percentage": round(
                    percentage,
                    1
                ),
                "recurrence": recurrence
            })

    # --------------------------------------------------------
    # Topic/problem relationships
    # --------------------------------------------------------

    relationship_counter = Counter()

    if (
        "Topics" in data.columns
        and "Problems" in data.columns
    ):

        for _, row in data.iterrows():

            topics = row.get(
                "Topics",
                []
            )

            problems = row.get(
                "Problems",
                []
            )

            if (
                isinstance(topics, list)
                and isinstance(problems, list)
            ):

                for topic in topics:

                    for problem in problems:

                        relationship_counter[
                            (topic, problem)
                        ] += 1

    relationships = []

    for (
        (topic, problem),
        count
    ) in relationship_counter.most_common():

        if count >= 2:

            relationships.append({
                "topic": topic,
                "problem": problem,
                "count": count
            })

    # --------------------------------------------------------
    # Pattern alerts
    # --------------------------------------------------------

    pattern_alerts = []

    negative_count = (
        data["Sentiment"] == "Negative"
    ).sum() if "Sentiment" in data.columns else 0

    negative_percent = (
        negative_count
        / max(1, total_reviews)
    ) * 100

    if negative_percent >= 40:

        pattern_alerts.append({
            "level": "CRITICAL",
            "title": "High dissatisfaction pattern",
            "message": (
                f"{negative_percent:.1f}% of analyzed reviews "
                "are negative."
            )
        })

    elif negative_percent >= 30:

        pattern_alerts.append({
            "level": "HIGH",
            "title": "High dissatisfaction pattern",
            "message": (
                f"{negative_percent:.1f}% of analyzed reviews "
                "are negative."
            )
        })

    elif negative_percent >= 20:

        pattern_alerts.append({
            "level": "MEDIUM",
            "title": "Moderate dissatisfaction pattern",
            "message": (
                f"{negative_percent:.1f}% of analyzed reviews "
                "are negative."
            )
        })

    if sentiment_trend["trend"] == "WORSENING":

        pattern_alerts.append({
            "level": "HIGH",
            "title": "Sentiment is worsening",
            "message": (
                "Customer sentiment is moving downward."
            )
        })

    for item in recurring_problems:

        if item["count"] >= 2:

            level = (
                "HIGH"
                if item["percentage"] >= 30
                else "MEDIUM"
            )

            pattern_alerts.append({
                "level": level,
                "title": (
                    f"Recurring problem: "
                    f"{item['problem']}"
                ),
                "message": (
                    f"Detected in {item['count']} reviews "
                    f"({item['percentage']:.1f}%)."
                )
            })

    return {
        "sentiment_trend": sentiment_trend,
        "recurring_problems": recurring_problems,
        "topic_problem_relationships": relationships,
        "pattern_alerts": pattern_alerts
    }


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

def generate_customer_intelligence(
    total_reviews,
    positive_count,
    neutral_count,
    negative_count,
    positive_percent,
    negative_percent,
    topic_counts,
    problem_counts
):

    action_plan = []

    action_map = {
        "Product Quality": (
            "Investigate product defects, quality-control procedures "
            "and product reliability.",
            "Improving product quality can reduce returns, "
            "complaints and negative feedback."
        ),

        "Delivery": (
            "Review fulfillment operations and delivery partner "
            "performance.",
            "Improving delivery reliability can reduce complaints "
            "and improve customer satisfaction."
        ),

        "Packaging": (
            "Improve packaging standards and product protection.",
            "Better packaging can reduce damaged-product complaints "
            "and replacement costs."
        ),

        "Price": (
            "Review pricing and customer-perceived value.",
            "Better price-value alignment can improve purchase "
            "satisfaction and retention."
        ),

        "Customer Service": (
            "Improve customer support response time and service quality.",
            "Better support can reduce unresolved complaints "
            "and improve customer trust."
        )
    }

    total_problem_count = sum(
        problem_counts.values()
    )

    for problem, count in sorted(
        problem_counts.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        percentage = (
            count
            / max(1, total_problem_count)
        ) * 100

        if percentage >= 50:
            priority = "CRITICAL"

        elif percentage >= 25:
            priority = "HIGH"

        elif percentage >= 10:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        action, impact = action_map.get(
            problem,
            (
                "Investigate the issue and identify "
                "corrective actions.",
                "Resolving the issue can improve customer experience."
            )
        )

        action_plan.append({
            "problem": problem,
            "priority": priority,
            "count": count,
            "percentage": round(
                percentage,
                1
            ),
            "action": action,
            "impact": impact
        })

    highest_priority_action = None

    if action_plan:

        priority_order = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        highest_priority_action = max(
            action_plan,
            key=lambda x: (
                priority_order.get(
                    x["priority"],
                    0
                ),
                x["count"]
            )
        )

    ai_insights = []

    if total_reviews > 0:

        ai_insights.append(
            "### 1. Executive Summary\n\n"
            f"An analysis of **{total_reviews} customer reviews** "
            f"shows **{positive_percent:.1f}% positive sentiment** "
            f"and **{negative_percent:.1f}% negative sentiment**."
        )

    if problem_counts:

        main_problem = max(
            problem_counts,
            key=problem_counts.get
        )

        main_problem_count = problem_counts[
            main_problem
        ]

        ai_insights.append(
            "### 2. Biggest Customer Problem\n\n"
            f"**{main_problem}** is the most significant detected "
            f"customer problem with **{main_problem_count} negative "
            "review detection(s)**."
        )

    if topic_counts:

        main_topic = max(
            topic_counts,
            key=topic_counts.get
        )

        main_topic_count = topic_counts[
            main_topic
        ]

        ai_insights.append(
            "### 3. Important Customer Trend\n\n"
            f"**{main_topic}** is the most frequently discussed topic "
            f"with **{main_topic_count} mention(s)**."
        )

    if negative_percent >= 30:

        ai_insights.append(
            "### 4. Business Risk\n\n"
            f"Negative feedback represents **{negative_percent:.1f}%** "
            "of the dataset. This indicates a meaningful customer "
            "experience risk that should be investigated."
        )

    else:

        ai_insights.append(
            "### 4. Business Risk\n\n"
            "The current negative feedback level is manageable, "
            "but recurring customer problems should continue to be monitored."
        )

    return {
        "ai_insights": ai_insights,
        "action_plan": action_plan,
        "highest_priority_action": highest_priority_action
    }


# ============================================================
# BUSINESS DECISION ENGINE
# ============================================================

def generate_business_decision_engine(
    problem_counts,
    problem_severity,
    root_cause_intelligence,
    trend_intelligence,
    action_plan,
    total_reviews,
    negative_percent
):

    if not problem_counts:

        return {
            "status": "MONITOR",
            "priority": "LOW",
            "severity_score": 0,
            "decision_confidence": 40,
            "related_occurrences": 0,
            "decision_chain": [
                "No major problem detected",
                "No root cause identified",
                "LOW",
                "Continue monitoring customer feedback.",
                "Maintain current customer experience."
            ],
            "reason": (
                "No significant customer problem was detected "
                "in the available reviews."
            ),
            "evidence": 0,
            "trend": trend_intelligence.get(
                "sentiment_trend",
                {}
            ).get(
                "trend",
                "NO DATA"
            ),
            "problem": "None",
            "root_cause": (
                "No root cause required."
            ),
            "recommended_action": (
                "Continue monitoring customer feedback."
            ),
            "expected_impact": (
                "Maintaining current performance while monitoring "
                "customer feedback."
            )
        }

    # --------------------------------------------------------
    # Highest severity problem
    # --------------------------------------------------------

    highest_problem = max(
        problem_severity,
        key=lambda x: problem_severity[x].get(
            "severity_score",
            0
        )
    )

    severity_data = problem_severity[
        highest_problem
    ]

    severity_score = severity_data.get(
        "severity_score",
        0
    )

    priority = severity_data.get(
        "priority",
        "LOW"
    )

    related_occurrences = severity_data.get(
        "negative_reviews",
        problem_counts.get(
            highest_problem,
            0
        )
    )

    # --------------------------------------------------------
    # Root cause
    # --------------------------------------------------------

    root_cause = (
        "Insufficient evidence to identify "
        "a specific root cause"
    )

    evidence = 0

    highest_root = root_cause_intelligence.get(
        "highest_priority_root_cause"
    )

    if highest_root:

        root_cause_data = highest_root.get(
            "root_cause"
        )

        if isinstance(
            root_cause_data,
            dict
        ):

            root_cause = root_cause_data.get(
                "cause",
                root_cause
            )

            evidence = root_cause_data.get(
                "evidence_count",
                0
            )

    # --------------------------------------------------------
    # Action
    # --------------------------------------------------------

    recommended_action = (
        "Investigate the identified customer problem "
        "and implement corrective action."
    )

    expected_impact = (
        "Resolving the issue can improve customer satisfaction "
        "and reduce negative feedback."
    )

    for item in action_plan:

        if item.get("problem") == highest_problem:

            recommended_action = item.get(
                "action",
                recommended_action
            )

            expected_impact = item.get(
                "impact",
                expected_impact
            )

            break

    # --------------------------------------------------------
    # Trend
    # --------------------------------------------------------

    trend = trend_intelligence.get(
        "sentiment_trend",
        {}
    ).get(
        "trend",
        "NO DATA"
    )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if priority == "CRITICAL":

        status = "ACT NOW"

    elif priority == "HIGH":

        status = "ACT SOON"

    elif priority == "MEDIUM":

        status = "PLAN"

    else:

        status = "MONITOR"

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = 50

    if related_occurrences >= 2:
        confidence += 10

    if evidence > 0:
        confidence += 20

    if trend == "WORSENING":
        confidence += 10

    if negative_percent >= 30:
        confidence += 5

    confidence = min(
        95,
        confidence
    )

    # --------------------------------------------------------
    # Rationale
    # --------------------------------------------------------

    if trend == "WORSENING":

        reason = (
            "The issue is supported by detected problem evidence "
            "and sentiment is worsening."
        )

    elif evidence > 0:

        reason = (
            "The issue is supported by repeated customer problem "
            "evidence and identifiable root-cause signals."
        )

    else:

        reason = (
            "The issue is supported by detected customer problem "
            "evidence, but the available reviews do not provide "
            "enough specific root-cause evidence."
        )

    return {
        "status": status,
        "priority": priority,
        "severity_score": severity_score,
        "decision_confidence": confidence,
        "related_occurrences": related_occurrences,
        "decision_chain": [
            highest_problem,
            root_cause,
            priority,
            recommended_action,
            expected_impact
        ],
        "reason": reason,
        "evidence": evidence,
        "trend": trend,
        "problem": highest_problem,
        "root_cause": root_cause,
        "recommended_action": recommended_action,
        "expected_impact": expected_impact
    }
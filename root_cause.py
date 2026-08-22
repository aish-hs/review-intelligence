# ==================================================
# ROOT CAUSE ANALYSIS MODULE
# ==================================================

ROOT_CAUSE_PATTERNS = {
    "Delivery": {
        "Delayed Shipping": [
            "slow delivery", "late delivery", "delivery delay",
            "delayed delivery", "took too long", "arrived late",
            "shipping delay", "long delivery time"
        ],
        "Poor Order Processing": [
            "order delayed", "processing delay", "dispatch delay",
            "shipment delayed", "order took too long"
        ],
        "Tracking Problems": [
            "tracking", "track order", "tracking not updated",
            "no tracking update", "wrong tracking"
        ]
    },
    "Product Quality": {
        "Defective Product": [
            "defective", "damaged", "broken", "not working",
            "stopped working", "faulty"
        ],
        "Poor Material Quality": [
            "poor quality", "bad quality", "cheap material",
            "low quality", "poor material"
        ],
        "Product Did Not Match Expectations": [
            "not as expected", "different from description",
            "not like the picture", "misleading description",
            "wrong product"
        ]
    },
    "Customer Service": {
        "Slow Support Response": [
            "no response", "slow response", "late response",
            "customer service slow", "support took too long"
        ],
        "Unhelpful Support": [
            "not helpful", "unhelpful", "support was useless",
            "customer service was useless"
        ],
        "Poor Communication": [
            "poor communication", "no communication",
            "did not inform", "not informed"
        ]
    },
    "Price": {
        "Product Overpriced": [
            "too expensive", "overpriced", "high price",
            "price is too high", "costly"
        ],
        "Poor Value for Money": [
            "not worth the price", "not worth it",
            "poor value", "waste of money"
        ]
    },
    "Packaging": {
        "Damaged Packaging": [
            "damaged packaging", "package damaged",
            "box damaged", "poor packaging"
        ],
        "Inadequate Protection": [
            "poorly packed", "not properly packed",
            "no protection", "insufficient packaging"
        ]
    }
}


def find_matching_causes(review, problem):
    """Find possible root causes for a specific customer problem."""
    if not review or problem not in ROOT_CAUSE_PATTERNS:
        return []

    review_text = str(review).lower()
    matched_causes = []

    for cause, keywords in ROOT_CAUSE_PATTERNS[problem].items():
        if any(keyword in review_text for keyword in keywords):
            matched_causes.append(cause)

    return matched_causes


def _get_review_column(data):
    """Support common review column names."""
    for column in ["Review", "review", "Reviews", "reviews", "Text", "text"]:
        if column in data.columns:
            return column
    return None


def analyze_root_causes(data, problem_severity):
    """Identify likely root causes behind detected customer problems."""
    results = []

    if data is None or data.empty or not problem_severity:
        return results

    review_column = _get_review_column(data)

    if review_column is None or "Problems" not in data.columns:
        return results

    sorted_problems = sorted(
        problem_severity.items(),
        key=lambda item: item[1].get("severity_score", 0),
        reverse=True
    )

    for problem, severity_info in sorted_problems:
        cause_counts = {}
        example_reviews = []

        for _, row in data.iterrows():
            detected_problems = row.get("Problems", "")

            if not detected_problems or str(detected_problems).lower() == "nan":
                continue

            problem_list = [
                item.strip()
                for item in str(detected_problems).split(",")
                if item.strip()
            ]

            if problem not in problem_list:
                continue

            review = row.get(review_column, "")
            matched_causes = find_matching_causes(review, problem)

            for cause in matched_causes:
                cause_counts[cause] = cause_counts.get(cause, 0) + 1

            if matched_causes and len(example_reviews) < 3:
                example_reviews.append(str(review))

        root_causes = [
            {"cause": cause, "evidence_count": count}
            for cause, count in sorted(
                cause_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ]

        if not root_causes:
            root_causes = [{
                "cause": "Insufficient evidence to identify a specific root cause",
                "evidence_count": 0
            }]

        results.append({
            "problem": problem,
            "priority": severity_info.get("priority", "LOW"),
            "severity_score": severity_info.get("severity_score", 0),
            "negative_reviews": severity_info.get("negative_reviews", 0),
            "root_causes": root_causes,
            "example_reviews": example_reviews
        })

    return results


def get_highest_priority_root_cause(root_cause_results):
    """Return the strongest root-cause finding for the highest-severity problem."""
    if not root_cause_results:
        return None

    highest_problem = root_cause_results[0]
    root_causes = highest_problem.get("root_causes", [])

    strongest_cause = None
    if root_causes:
        strongest_cause = max(
            root_causes,
            key=lambda item: item.get("evidence_count", 0)
        )

    return {
        "problem": highest_problem.get("problem"),
        "priority": highest_problem.get("priority"),
        "severity_score": highest_problem.get("severity_score"),
        "root_cause": strongest_cause
    }
# ==================================================
# BUSINESS SUMMARY MODULE
# ==================================================


# ==================================================
# GENERATE BUSINESS HEALTH
# ==================================================

def calculate_business_health(
    negative_percent,
    satisfaction_score
):

    if (
        negative_percent >= 40
        or satisfaction_score < 40
    ):

        return (
            "CRITICAL",
            "🔴 Customer experience requires immediate attention."
        )

    elif (
        negative_percent >= 25
        or satisfaction_score < 60
    ):

        return (
            "HIGH",
            "🟠 Customer experience needs significant improvement."
        )

    elif (
        negative_percent >= 15
        or satisfaction_score < 75
    ):

        return (
            "MEDIUM",
            "🟡 Customer experience is acceptable but has areas for improvement."
        )

    else:

        return (
            "LOW",
            "🟢 Customer experience is generally healthy."
        )


# ==================================================
# GENERATE BUSINESS SUMMARY
# ==================================================

def generate_business_summary(
    total_reviews,
    positive_percent,
    negative_percent,
    satisfaction_score,
    topic_counts,
    problem_counts,
    highest_priority_action
):

    # ==================================================
    # MAIN TOPIC
    # ==================================================

    if topic_counts:

        main_topic = max(
            topic_counts,
            key=topic_counts.get
        )

        main_topic_count = topic_counts[
            main_topic
        ]

    else:

        main_topic = "None identified"

        main_topic_count = 0


    # ==================================================
    # MAIN CUSTOMER PROBLEM
    # ==================================================

    if problem_counts:

        main_problem = max(
            problem_counts,
            key=problem_counts.get
        )

        main_problem_count = problem_counts[
            main_problem
        ]

    else:

        main_problem = "No major problem detected"

        main_problem_count = 0


    # ==================================================
    # BUSINESS HEALTH
    # ==================================================

    health_level, health_message = (
        calculate_business_health(
            negative_percent,
            satisfaction_score
        )
    )


    # ==================================================
    # PRIORITY INFORMATION
    # ==================================================

    if highest_priority_action:

        priority = highest_priority_action.get(
            "priority",
            "LOW"
        )

        recommended_action = (
            highest_priority_action.get(
                "action",
                "Continue monitoring customer feedback."
            )
        )

        expected_impact = (
            highest_priority_action.get(
                "impact",
                "Maintaining customer satisfaction."
            )
        )

    else:

        priority = "LOW"

        recommended_action = (
            "Continue monitoring customer feedback."
        )

        expected_impact = (
            "Maintaining a positive customer experience."
        )


    # ==================================================
    # RETURN BUSINESS SUMMARY
    # ==================================================

    return {

        "total_reviews": total_reviews,

        "business_health": health_level,

        "health_message": health_message,

        "positive_percent": round(
            positive_percent,
            1
        ),

        "negative_percent": round(
            negative_percent,
            1
        ),

        "satisfaction_score": satisfaction_score,

        "main_topic": main_topic,

        "main_topic_count": main_topic_count,

        "main_problem": main_problem,

        "main_problem_count": main_problem_count,

        "priority": priority,

        "recommended_action": recommended_action,

        "expected_impact": expected_impact

    }
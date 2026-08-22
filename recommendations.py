# ==================================================
# RECOMMENDATIONS
# ==================================================

def generate_recommendations(
    aspects,
    sentiment
):

    recommendations = []

    if "Delivery" in aspects:

        recommendations.append(
            "🚚 Improve delivery speed and reduce shipping delays."
        )

    if "Packaging" in aspects:

        recommendations.append(
            "📦 Improve packaging protection to prevent product damage."
        )

    if "Price" in aspects:

        recommendations.append(
            "💰 Review pricing and improve value for money."
        )

    if "Product Quality" in aspects:

        if sentiment == "Negative":

            recommendations.append(
                "🔧 Investigate product quality issues."
            )

        else:

            recommendations.append(
                "⭐ Maintain the current product quality."
            )

    if "Customer Service" in aspects:

        recommendations.append(
            "☎️ Improve customer support response time."
        )

    return recommendations


# ==================================================
# PRIORITY RECOMMENDATION
# ==================================================

def get_priority_recommendation(
    problem_counts
):

    if not problem_counts:

        return (
            None,
            0,
            "🎉 No major customer problems detected."
        )

    priority_problem = max(
        problem_counts,
        key=problem_counts.get
    )

    priority_count = (
        problem_counts[
            priority_problem
        ]
    )

    recommendations = {

        "Delivery":
            "🚚 Prioritize improving delivery speed "
            "and reducing delays.",

        "Product Quality":
            "🔧 Investigate product quality issues "
            "and improve reliability.",

        "Packaging":
            "📦 Improve packaging protection "
            "and reduce damage during shipping.",

        "Price":
            "💰 Review pricing and improve "
            "value for money.",

        "Customer Service":
            "☎️ Improve customer support response "
            "time and service quality."
    }

    recommendation = recommendations.get(
        priority_problem,
        "🔍 Investigate this issue and monitor "
        "future customer feedback."
    )

    return (
        priority_problem,
        priority_count,
        recommendation
    )
# ==================================================
# AI INSIGHTS MODULE
# ==================================================

from llm_service import generate_ai_response


# ==================================================
# LOCAL FALLBACK INSIGHTS
# ==================================================

def generate_fallback_insights(
    total_reviews,
    positive_count,
    neutral_count,
    negative_count,
    positive_percent,
    negative_percent,
    satisfaction_score,
    topic_counts,
    problem_counts
):

    insights = []


    # ==================================================
    # OVERALL CUSTOMER SENTIMENT
    # ==================================================

    if negative_percent >= 40:

        insights.append(
            "🚨 Customer dissatisfaction is high. "
            "Immediate action should be taken to "
            "identify and resolve the major customer problems."
        )

    elif negative_percent >= 20:

        insights.append(
            "⚠️ A noticeable portion of customers "
            "are dissatisfied. The business should "
            "investigate the main sources of negative feedback."
        )

    else:

        insights.append(
            "✅ Overall customer sentiment is positive. "
            "The business should continue maintaining "
            "the current customer experience."
        )


    # ==================================================
    # SATISFACTION SCORE
    # ==================================================

    if satisfaction_score >= 80:

        satisfaction_message = (
            "🌟 Customer satisfaction is excellent."
        )

    elif satisfaction_score >= 60:

        satisfaction_message = (
            "👍 Customer satisfaction is at a good level, "
            "but some improvement opportunities remain."
        )

    elif satisfaction_score >= 40:

        satisfaction_message = (
            "⚠️ Customer satisfaction needs improvement."
        )

    else:

        satisfaction_message = (
            "🚨 Customer satisfaction is critically low."
        )


    insights.append(
        f"⭐ **Satisfaction Score:** "
        f"{satisfaction_score}/100. "
        f"{satisfaction_message}"
    )


    # ==================================================
    # MOST DISCUSSED TOPIC
    # ==================================================

    if topic_counts:

        main_topic = max(
            topic_counts,
            key=topic_counts.get
        )

        main_topic_count = topic_counts[
            main_topic
        ]

        topic_percentage = (
            main_topic_count /
            max(1, total_reviews)
        ) * 100

        insights.append(
            f"🔍 **Most discussed area:** {main_topic}. "
            f"It was mentioned in {main_topic_count} "
            f"reviews ({topic_percentage:.1f}% of all reviews)."
        )


    # ==================================================
    # BIGGEST CUSTOMER PROBLEM
    # ==================================================

    if problem_counts:

        biggest_problem = max(
            problem_counts,
            key=problem_counts.get
        )

        biggest_problem_count = (
            problem_counts[
                biggest_problem
            ]
        )

        insights.append(
            f"🚨 **Biggest customer problem:** "
            f"{biggest_problem}. "
            f"It appears in {biggest_problem_count} "
            f"negative reviews."
        )

    else:

        biggest_problem = None

        insights.append(
            "🎉 No major customer problems were "
            "identified from the negative reviews."
        )


    # ==================================================
    # PRIORITY LEVEL
    # ==================================================

    if negative_percent >= 40:

        priority = "🔴 HIGH PRIORITY"

        priority_message = (
            "Immediate investigation and corrective "
            "action are recommended."
        )

    elif negative_percent >= 20:

        priority = "🟠 MEDIUM PRIORITY"

        priority_message = (
            "The business should monitor these issues "
            "and take corrective action."
        )

    else:

        priority = "🟢 LOW PRIORITY"

        priority_message = (
            "No urgent intervention is required, "
            "but customer feedback should continue "
            "to be monitored."
        )


    insights.append(
        f"🎯 **Priority Level:** {priority}. "
        f"{priority_message}"
    )


    # ==================================================
    # BUSINESS RECOMMENDATION
    # ==================================================

    if problem_counts:

        if biggest_problem == "Delivery":

            recommendation = (
                "🚚 Improve delivery speed, "
                "logistics coordination and "
                "shipment tracking."
            )

        elif biggest_problem == "Product Quality":

            recommendation = (
                "🔧 Investigate product defects, "
                "quality-control processes and "
                "product reliability."
            )

        elif biggest_problem == "Packaging":

            recommendation = (
                "📦 Improve packaging protection "
                "to reduce damage during transportation."
            )

        elif biggest_problem == "Price":

            recommendation = (
                "💰 Review pricing and improve "
                "the perceived value for money."
            )

        elif biggest_problem == "Customer Service":

            recommendation = (
                "☎️ Improve customer support "
                "response time and service quality."
            )

        else:

            recommendation = (
                "🔍 Investigate the identified "
                "customer problem and monitor "
                "future feedback."
            )


        insights.append(
            f"💡 **Recommended Business Action:** "
            f"{recommendation}"
        )


    return insights


# ==================================================
# REAL AI INSIGHTS
# ==================================================

def generate_real_ai_insight(
    total_reviews,
    positive_count,
    neutral_count,
    negative_count,
    positive_percent,
    negative_percent,
    satisfaction_score,
    topic_counts,
    problem_counts
):

    # ==================================================
    # PREPARE STRUCTURED AI PROMPT
    # ==================================================

    prompt = f"""
You are an expert Business Intelligence Analyst
specializing in Customer Experience and Review Analytics.

Analyze the customer review data below.

==============================
CUSTOMER OVERVIEW
==============================

Total Reviews:
{total_reviews}

Positive Reviews:
{positive_count}

Neutral Reviews:
{neutral_count}

Negative Reviews:
{negative_count}

Positive Percentage:
{positive_percent:.1f}%

Negative Percentage:
{negative_percent:.1f}%

Customer Satisfaction Score:
{satisfaction_score}/100


==============================
TOPIC FREQUENCY
==============================

{topic_counts}


==============================
CUSTOMER PROBLEMS
==============================

{problem_counts}


==============================
YOUR TASK
==============================

Generate a concise but useful business intelligence report.

Use exactly these sections:

1. Executive Summary
2. Customer Satisfaction
3. Biggest Customer Problem
4. Important Customer Trend
5. Business Impact
6. Priority Level
7. Recommended Actions


==============================
ANALYSIS RULES
==============================

- Base conclusions only on the supplied statistics.
- Do not invent customer complaints.
- Do not invent statistics.
- Clearly distinguish facts from business interpretation.
- Identify the most important problem based on the supplied data.
- Consider both negative percentage and satisfaction score.
- Mention important topic patterns when supported by the data.
- Give practical and realistic business recommendations.
- Recommendations should directly address the identified problems.
- Keep the report suitable for a business manager.
- Use simple professional English.
- Use bullet points where useful.
- Do not mention that you are an AI.
- Do not repeat the raw data unnecessarily.
- Keep the report concise but meaningful.
"""


    # ==================================================
    # CALL GEMINI THROUGH LLM SERVICE
    # ==================================================

    try:

        result = generate_ai_response(
            prompt
        )

        if not result:

            return None

        return result.strip()


    except Exception as error:

        print(
            f"AI API error: {error}"
        )

        return None


# ==================================================
# MAIN AI INSIGHT FUNCTION
# ==================================================

def generate_ai_insights(
    total_reviews,
    positive_count,
    neutral_count,
    negative_count,
    positive_percent,
    negative_percent,
    satisfaction_score,
    topic_counts,
    problem_counts
):

    # ==================================================
    # TRY REAL AI FIRST
    # ==================================================

    real_ai_result = generate_real_ai_insight(

        total_reviews,

        positive_count,

        neutral_count,

        negative_count,

        positive_percent,

        negative_percent,

        satisfaction_score,

        topic_counts,

        problem_counts

    )


    if real_ai_result:

        return [
            "🧠 **Real AI Analysis**\n\n"
            + real_ai_result
        ]


    # ==================================================
    # FALLBACK
    # ==================================================

    fallback_result = generate_fallback_insights(

        total_reviews,

        positive_count,

        neutral_count,

        negative_count,

        positive_percent,

        negative_percent,

        satisfaction_score,

        topic_counts,

        problem_counts

    )


    return fallback_result
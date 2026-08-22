import streamlit as st
import pandas as pd

from main import (
    detect_aspects,
    analyze_sentiment,
    generate_recommendations,
    analyze_reviews,
    get_topic_counts,
    get_problem_counts,
    get_priority_recommendation,
    generate_executive_summary,
    calculate_satisfaction,
    generate_business_insight,
    generate_customer_intelligence
)


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Review Intelligence",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Review Intelligence")
st.write("AI-powered customer review analysis")


# ==================================================
# SINGLE REVIEW
# ==================================================

st.header("📝 Analyze a Single Review")

review = st.text_area(
    "Enter a customer review:",
    placeholder=(
        "Example: The product quality is excellent, "
        "but delivery was very slow."
    )
)

if st.button("Analyze Single Review"):

    if review.strip():

        sentiment, polarity = analyze_sentiment(
            review
        )

        aspects = detect_aspects(
            review
        )

        st.subheader("📊 Analysis Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Sentiment",
                sentiment
            )

        with col2:

            st.metric(
                "Sentiment Score",
                round(polarity, 2)
            )

        st.write("### 🔍 Topics Detected")

        if aspects:

            for aspect in aspects:

                st.write(
                    "•",
                    aspect
                )

        else:

            st.write(
                "No specific topic detected."
            )

        recommendations = generate_recommendations(
            aspects,
            sentiment
        )

        st.write(
            "### 💡 Recommended Actions"
        )

        if recommendations:

            for recommendation in recommendations:

                st.write(
                    "•",
                    recommendation
                )

        else:

            st.write(
                "No major action required."
            )

    else:

        st.warning(
            "Please enter a review."
        )


# ==================================================
# MULTIPLE REVIEWS
# ==================================================

st.divider()

st.header("📁 Analyze Multiple Reviews")

st.write(
    "Upload a CSV file containing customer reviews."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    data = pd.read_csv(
        uploaded_file
    )

    st.success(
        "CSV uploaded successfully! ✅"
    )

    st.write("### Preview")

    st.dataframe(
        data.head()
    )


    # ==================================================
    # FIND REVIEW COLUMN
    # ==================================================

    possible_columns = [
        "review",
        "reviews",
        "text",
        "comment",
        "feedback"
    ]

    review_column = None

    for column in data.columns:

        if column.lower() in possible_columns:

            review_column = column

            break


    if review_column is None:

        st.error(
            "Could not find a review column. "
            "Please name your column 'review'."
        )

    else:

        # ==================================================
        # ANALYZE REVIEWS
        # ==================================================

        data = analyze_reviews(
            data,
            review_column
        )

        st.success(
            f"Successfully analyzed {len(data)} reviews! 🎉"
        )


        # ==================================================
        # REVIEW DASHBOARD
        # ==================================================

        st.header(
            "📊 Review Dashboard"
        )

        positive_count = (
            data["Sentiment"] == "Positive"
        ).sum()

        neutral_count = (
            data["Sentiment"] == "Neutral"
        ).sum()

        negative_count = (
            data["Sentiment"] == "Negative"
        ).sum()


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Reviews",
                len(data)
            )

        with col2:

            st.metric(
                "😊 Positive",
                positive_count
            )

        with col3:

            st.metric(
                "😐 Neutral",
                neutral_count
            )

        with col4:

            st.metric(
                "😞 Negative",
                negative_count
            )


        # ==================================================
        # SENTIMENT DISTRIBUTION
        # ==================================================

        st.subheader(
            "😊 Sentiment Distribution"
        )

        total_reviews = len(data)

        positive_percent = (
            positive_count /
            max(1, total_reviews)
        ) * 100

        neutral_percent = (
            neutral_count /
            max(1, total_reviews)
        ) * 100

        negative_percent = (
            negative_count /
            max(1, total_reviews)
        ) * 100

        average_score = data[
            "Sentiment Score"
        ].mean()


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "😊 Positive",
                f"{positive_percent:.1f}%"
            )

        with col2:

            st.metric(
                "😐 Neutral",
                f"{neutral_percent:.1f}%"
            )

        with col3:

            st.metric(
                "😞 Negative",
                f"{negative_percent:.1f}%"
            )


        st.metric(
            "📈 Average Sentiment Score",
            f"{average_score:.2f}"
        )


        # ==================================================
        # SENTIMENT CHART
        # ==================================================

        sentiment_chart = pd.DataFrame({

            "Sentiment": [
                "Positive",
                "Neutral",
                "Negative"
            ],

            "Reviews": [
                positive_count,
                neutral_count,
                negative_count
            ]

        })


        st.bar_chart(
            sentiment_chart.set_index(
                "Sentiment"
            )
        )


        # ==================================================
        # TOPIC FREQUENCY
        # ==================================================

        st.subheader(
            "🔍 Most Mentioned Topics"
        )

        topic_counts = get_topic_counts(
            data
        )


        if topic_counts:

            topic_df = pd.DataFrame(
                list(
                    topic_counts.items()
                ),
                columns=[
                    "Topic",
                    "Mentions"
                ]
            )

            topic_df = topic_df.sort_values(
                "Mentions",
                ascending=False
            )

            st.bar_chart(
                topic_df.set_index(
                    "Topic"
                )
            )

        else:

            st.info(
                "No topics detected."
            )


        # ==================================================
        # CUSTOMER PROBLEMS
        # ==================================================

        st.subheader(
            "🚨 Customer Problems Detected"
        )

        problem_counts = get_problem_counts(
            data
        )

        negative_reviews = data[
            data["Sentiment"] == "Negative"
        ]


        if len(negative_reviews) > 0:

            if problem_counts:

                problem_df = pd.DataFrame(
                    list(
                        problem_counts.items()
                    ),
                    columns=[
                        "Problem",
                        "Negative Reviews"
                    ]
                )

                problem_df = problem_df.sort_values(
                    "Negative Reviews",
                    ascending=False
                )

                st.write(
                    "The following topics are causing "
                    "the most negative feedback:"
                )

                st.dataframe(
                    problem_df,
                    width="stretch"
                )

                biggest_problem = (
                    problem_df.iloc[0]
                )

                st.warning(
                    f"🚨 **Main Customer Problem:** "
                    f"{biggest_problem['Problem']} "
                    f"({biggest_problem['Negative Reviews']} "
                    f"negative reviews)"
                )

            else:

                st.info(
                    "Negative reviews were found, "
                    "but no specific problem topics "
                    "were detected."
                )

        else:

            st.success(
                "🎉 No negative reviews detected!"
            )


        # ==================================================
        # EXECUTIVE SUMMARY
        # ==================================================

        st.subheader(
            "🤖 Executive Summary"
        )

        if total_reviews > 0:

            summary = generate_executive_summary(
                positive_percent,
                negative_percent,
                topic_counts
            )

            st.info(
                summary
            )

        else:

            st.info(
                "No reviews available for analysis."
            )


        # ==================================================
        # CUSTOMER SATISFACTION SCORE
        # ==================================================

        st.subheader(
            "⭐ Overall Customer Satisfaction"
        )

        (
            satisfaction_score,
            score_message
        ) = calculate_satisfaction(

            positive_count,

            neutral_count,

            negative_count,

            total_reviews

        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "⭐ Satisfaction Score",
                f"{satisfaction_score}/100"
            )

        with col2:

            st.write(
                f"### {score_message}"
            )


        # ==================================================
        # PRIORITY RECOMMENDATIONS
        # ==================================================

        st.subheader(
            "🎯 Priority Recommendations"
        )

        (
            priority_problem,
            priority_count,
            recommendation
        ) = get_priority_recommendation(
            problem_counts
        )


        if priority_problem:

            st.warning(
                f"🚨 **Priority Issue:** "
                f"{priority_problem}"
            )

            st.write(
                f"**Negative reviews:** "
                f"{priority_count}"
            )

            st.info(
                f"💡 **Recommended Action:** "
                f"{recommendation}"
            )

        else:

            st.success(
                recommendation
            )


        # ==================================================
        # SENTIMENT TREND
        # ==================================================

        st.subheader(
            "📈 Sentiment Trend"
        )


        if len(data) > 1:

            trend_data = data[
                ["Sentiment Score"]
            ].copy()

            trend_data.index = range(
                1,
                len(trend_data) + 1
            )

            trend_data.index.name = (
                "Review Number"
            )

            st.line_chart(
                trend_data
            )

            st.caption(
                "The chart shows how sentiment scores "
                "vary across customer reviews."
            )

        else:

            st.info(
                "At least two reviews are required "
                "to display a sentiment trend."
            )


        # ==================================================
        # DETAILED RESULTS
        # ==================================================

        st.subheader(
            "📋 Detailed Results"
        )

        st.dataframe(
            data,
            width="stretch"
        )


        # ==================================================
        # DOWNLOAD RESULTS
        # ==================================================

        csv = data.to_csv(
            index=False
        )

        st.download_button(

            label="⬇️ Download Analysis",

            data=csv,

            file_name="review_analysis.csv",

            mime="text/csv"

        )


        # ==================================================
        # BUSINESS INSIGHTS
        # ==================================================

        st.subheader(
            "💼 Business Insights"
        )

        business_insight = (
            generate_business_insight(
                negative_percent
            )
        )

        if negative_percent >= 40:

            st.error(
                business_insight
            )

        elif negative_percent >= 20:

            st.warning(
                business_insight
            )

        else:

            st.success(
                business_insight
            )


        # ==================================================
        # MOST IMPORTANT TOPIC
        # ==================================================

        if topic_counts:

            main_topic = max(
                topic_counts,
                key=topic_counts.get
            )

            st.write(
                f"🔎 **Most discussed area:** "
                f"{main_topic}"
            )

            st.write(
                f"📊 **Mentions:** "
                f"{topic_counts[main_topic]}"
            )


        # ==================================================
        # PRIORITY PROBLEM
        # ==================================================

        if problem_counts:

            priority_problem = max(
                problem_counts,
                key=problem_counts.get
            )

            st.write(
                f"🚨 **Most common customer problem:** "
                f"{priority_problem}"
            )

            st.write(
                f"📌 **Negative reviews mentioning it:** "
                f"{problem_counts[priority_problem]}"
            )


        # ==================================================
        # CUSTOMER INTELLIGENCE PIPELINE
        # ==================================================

        customer_intelligence = (
            generate_customer_intelligence(

                total_reviews,

                positive_count,

                neutral_count,

                negative_count,

                positive_percent,

                negative_percent,

                topic_counts,

                problem_counts

            )
        )


        # ==================================================
        # AI-POWERED BUSINESS INSIGHTS
        # ==================================================

        st.divider()

        st.subheader(
            "🤖 AI-Powered Business Insights"
        )

        ai_insights = customer_intelligence[
            "ai_insights"
        ]

        for insight in ai_insights:

            st.info(
                insight
            )


        # ==================================================
        # CUSTOMER ACTION CENTER
        # ==================================================

        st.divider()

        st.subheader(
            "🎯 Customer Action Center"
        )

        st.write(
            "Convert customer feedback into "
            "specific business actions."
        )


        action_plan = customer_intelligence[
            "action_plan"
        ]

        highest_priority_action = (
            customer_intelligence[
                "highest_priority_action"
            ]
        )


        # ==================================================
        # HIGHEST PRIORITY ACTION
        # ==================================================

        if highest_priority_action:

            st.write(
                "### 🚨 Highest Priority Action"
            )

            priority = (
                highest_priority_action[
                    "priority"
                ]
            )

            problem = (
                highest_priority_action[
                    "problem"
                ]
            )

            action = (
                highest_priority_action[
                    "action"
                ]
            )

            impact = (
                highest_priority_action[
                    "impact"
                ]
            )


            if priority == "CRITICAL":

                st.error(
                    f"🔴 **{priority} PRIORITY**"
                )

            elif priority == "HIGH":

                st.warning(
                    f"🟠 **{priority} PRIORITY**"
                )

            elif priority == "MEDIUM":

                st.info(
                    f"🟡 **{priority} PRIORITY**"
                )

            else:

                st.success(
                    f"🟢 **{priority} PRIORITY**"
                )


            st.write(
                f"### Problem: {problem}"
            )

            st.write(
                f"**Recommended Action:** {action}"
            )

            st.write(
                f"**Expected Business Impact:** {impact}"
            )


        # ==================================================
        # COMPLETE ACTION PLAN
        # ==================================================

        st.write(
            "### 📋 Complete Action Plan"
        )


        if action_plan:

            for index, action_item in enumerate(
                action_plan,
                start=1
            ):

                priority = action_item[
                    "priority"
                ]

                problem = action_item[
                    "problem"
                ]

                count = action_item.get(
                    "count",
                    0
                )

                percentage = action_item.get(
                    "percentage",
                    0
                )

                action = action_item[
                    "action"
                ]

                impact = action_item[
                    "impact"
                ]


                with st.expander(
                    f"{index}. {problem} — {priority}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Priority",
                            priority
                        )

                    with col2:

                        st.metric(
                            "Negative Reviews",
                            count
                        )


                    st.write(
                        f"**Problem:** {problem}"
                    )

                    st.write(
                        f"**Share of detected problems:** "
                        f"{percentage}%"
                    )

                    st.write(
                        f"**Action:** {action}"
                    )

                    st.write(
                        f"**Expected Impact:** {impact}"
                    )


        else:

            st.success(
                "No action items were generated."
            )


        # ==================================================
        # BUSINESS DECISION SUMMARY
        # ==================================================

        st.divider()

        st.header(
            "📊 Business Decision Summary"
        )

        st.write(
            "A consolidated view of customer "
            "experience, business health and "
            "recommended action."
        )

        business_summary = (
            customer_intelligence[
                "business_summary"
            ]
        )


        # ==================================================
        # SUMMARY METRICS
        # ==================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏥 Business Health",
                business_summary[
                    "business_health"
                ]
            )

        with col2:

            st.metric(
                "⭐ Satisfaction",
                f"{business_summary['satisfaction_score']}/100"
            )

        with col3:

            st.metric(
                "😊 Positive",
                f"{business_summary['positive_percent']:.1f}%"
            )

        with col4:

            st.metric(
                "😞 Negative",
                f"{business_summary['negative_percent']:.1f}%"
            )


        # ==================================================
        # HEALTH MESSAGE
        # ==================================================

        health_level = (
            business_summary[
                "business_health"
            ]
        )

        health_message = (
            business_summary[
                "health_message"
            ]
        )


        if health_level == "CRITICAL":

            st.error(
                health_message
            )

        elif health_level == "HIGH":

            st.warning(
                health_message
            )

        elif health_level == "MEDIUM":

            st.info(
                health_message
            )

        else:

            st.success(
                health_message
            )


        # ==================================================
        # KEY BUSINESS FINDINGS
        # ==================================================

        st.subheader(
            "🔎 Key Business Findings"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "### 🔍 Most Discussed Topic"
            )

            st.write(
                f"**{business_summary['main_topic']}**"
            )

            st.write(
                f"Mentions: "
                f"{business_summary['main_topic_count']}"
            )


        with col2:

            st.write(
                "### 🚨 Main Customer Problem"
            )

            st.write(
                f"**{business_summary['main_problem']}**"
            )

            st.write(
                f"Negative reviews: "
                f"{business_summary['main_problem_count']}"
            )


        # ==================================================
        # FINAL BUSINESS ACTION
        # ==================================================

        st.subheader(
            "🎯 Final Business Action"
        )

        st.write(
            f"**Priority:** "
            f"{business_summary['priority']}"
        )

        st.info(
            f"💡 **Recommended Action:** "
            f"{business_summary['recommended_action']}"
        )

        st.success(
            f"📈 **Expected Business Impact:** "
            f"{business_summary['expected_impact']}"
        )
import streamlit as st
import pandas as pd
from io import BytesIO

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
    generate_customer_intelligence,
    get_topic_sentiment_analysis,
    get_problem_severity_analysis,
    get_highest_severity_problem,
    generate_root_cause_intelligence,
    generate_advanced_trend_intelligence,
    generate_business_decision_engine
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Review Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #111827 50%,
                #0b1120 100%
            );
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
    }

    p {
        color: #cbd5e1;
    }

    .dashboard-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #f8fafc;
        margin-top: 25px;
        margin-bottom: 16px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 18px;
    }

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #1e293b,
                #172033
            );
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }

    .stTextArea textarea::placeholder {
        color: #64748b !important;
    }

    .stFileUploader section {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
    }

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed
            );
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 10px 20px;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stExpander"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
    }

    hr {
        border-color: #334155 !important;
    }

    .dashboard-footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #1e293b;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">🔍 Review Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'AI-powered customer review analysis and '
    'business decision intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SINGLE REVIEW ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📝 Analyze a Single Customer Review</div>',
    unsafe_allow_html=True
)

review = st.text_area(
    "Enter customer review",
    placeholder=(
        "Example: The product quality is excellent, "
        "but delivery was very slow."
    ),
    height=120
)


if st.button("🔍 Analyze Single Review"):

    if review.strip():

        try:

            sentiment, polarity = analyze_sentiment(review)
            aspects = detect_aspects(review)

            st.markdown(
                '<div class="section-title">📊 Analysis Result</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "😊 SENTIMENT",
                    sentiment
                )

            with col2:
                st.metric(
                    "📈 SENTIMENT SCORE",
                    f"{polarity:.2f}"
                )

            st.markdown("### 🔎 Topics Detected")

            if aspects:

                for aspect in aspects:
                    st.write(f"• {aspect}")

            else:

                st.info(
                    "No specific topic detected."
                )

            recommendations = generate_recommendations(
                aspects,
                sentiment
            )

            st.markdown("### 💡 Recommended Actions")

            if recommendations:

                for recommendation in recommendations:
                    st.write(
                        f"• {recommendation}"
                    )

            else:

                st.success(
                    "No major action required."
                )

        except Exception as error:

            st.error(
                f"❌ Unable to analyze the review: {error}"
            )

    else:

        st.warning(
            "Please enter a review."
        )


# ============================================================
# DATASET SECTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📁 Customer Review Dataset</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload a CSV file containing customer reviews.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    # ========================================================
    # LOAD CSV SAFELY
    # ========================================================

    try:

        data = pd.read_csv(
            uploaded_file
        )

    except Exception as error:

        st.error(
            f"❌ Unable to read CSV file: {error}"
        )

        st.stop()


    # ========================================================
    # VALIDATE DATASET
    # ========================================================

    if data.empty:

        st.error(
            "❌ The uploaded CSV file is empty. "
            "Please upload a CSV containing customer reviews."
        )

        st.stop()


    st.success(
        "CSV uploaded successfully! ✅"
    )


    # ========================================================
    # FIND REVIEW COLUMN
    # ========================================================

    possible_columns = [
        "review",
        "reviews",
        "text",
        "comment",
        "feedback"
    ]

    review_column = None

    for column in data.columns:

        if column.lower().strip() in possible_columns:

            review_column = column
            break


    if review_column is None:

        st.error(
            "Could not find a review column. "
            "Please name your column 'review'."
        )

        st.stop()


    # ========================================================
    # ANALYZE REVIEWS SAFELY
    # ========================================================

    try:

        data = analyze_reviews(
            data,
            review_column
        )

    except Exception as error:

        st.error(
            f"❌ Unable to analyze the uploaded reviews: {error}"
        )

        st.stop()


    # ========================================================
    # BASIC COUNTS
    # ========================================================

    total_reviews = len(data)

    positive_count = (
        data["Sentiment"] == "Positive"
    ).sum()

    neutral_count = (
        data["Sentiment"] == "Neutral"
    ).sum()

    negative_count = (
        data["Sentiment"] == "Negative"
    ).sum()


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


    # ========================================================
    # SATISFACTION
    # ========================================================

    satisfaction_score, score_message = calculate_satisfaction(
        positive_count,
        neutral_count,
        negative_count,
        total_reviews
    )


    # ========================================================
    # TOPICS
    # ========================================================

    topic_counts = get_topic_counts(
        data
    )


    # ========================================================
    # TOPIC-WISE SENTIMENT
    # ========================================================

    topic_sentiment = get_topic_sentiment_analysis(
        data
    )


    # ========================================================
    # PROBLEMS
    # ========================================================

    problem_counts = get_problem_counts(
        data
    )


    # ========================================================
    # PROBLEM SEVERITY & PRIORITY
    # ========================================================

    problem_severity = get_problem_severity_analysis(
        problem_counts=problem_counts,
        total_reviews=total_reviews,
        negative_count=negative_count
    )

    highest_severity_problem = get_highest_severity_problem(
        problem_severity
    )


    # ========================================================
    # ROOT CAUSE INTELLIGENCE
    # ========================================================

    root_cause_intelligence = (
        generate_root_cause_intelligence(
            data=data,
            problem_severity=problem_severity
        )
    )

    root_cause_analysis = (
        root_cause_intelligence.get(
            "root_cause_analysis",
            []
        )
    )

    highest_priority_root_cause = (
        root_cause_intelligence.get(
            "highest_priority_root_cause"
        )
    )


    # ========================================================
    # ADVANCED TREND & PATTERN INTELLIGENCE
    # ========================================================

    trend_intelligence = generate_advanced_trend_intelligence(
        data=data,
        problem_counts=problem_counts,
        total_reviews=total_reviews
    )

    sentiment_trend_analysis = trend_intelligence.get(
        "sentiment_trend",
        {}
    )

    recurring_problems = trend_intelligence.get(
        "recurring_problems",
        []
    )

    topic_problem_relationships = trend_intelligence.get(
        "topic_problem_relationships",
        []
    )

    pattern_alerts = trend_intelligence.get(
        "pattern_alerts",
        []
    )


    # ========================================================
    # BUSINESS HEALTH
    # ========================================================

    if negative_percent >= 40:

        business_health = "CRITICAL"

        health_message = (
            "Customer dissatisfaction is critically high."
        )

    elif negative_percent >= 30:

        business_health = "HIGH"

        health_message = (
            "Customer experience needs significant improvement."
        )

    elif negative_percent >= 20:

        business_health = "MEDIUM"

        health_message = (
            "Some customer experience issues require attention."
        )

    else:

        business_health = "LOW"

        health_message = (
            "Customer experience is generally healthy."
        )


    # ========================================================
    # MAIN TOPIC
    # ========================================================

    if topic_counts:

        main_topic = max(
            topic_counts,
            key=topic_counts.get
        )

        main_topic_count = topic_counts[
            main_topic
        ]

    else:

        main_topic = "None"
        main_topic_count = 0


    # ========================================================
    # MAIN PROBLEM
    # ========================================================

    if problem_counts:

        main_problem = max(
            problem_counts,
            key=problem_counts.get
        )

        main_problem_count = problem_counts[
            main_problem
        ]

    else:

        main_problem = "None"
        main_problem_count = 0


    # ========================================================
    # PRIORITY RECOMMENDATION
    # ========================================================

    (
        priority_problem,
        priority_count,
        priority_recommendation
    ) = get_priority_recommendation(
        problem_counts
    )


    if priority_problem:

        if negative_percent >= 40:

            final_priority = "CRITICAL"

        elif negative_percent >= 20:

            final_priority = "HIGH"

        else:

            final_priority = "MEDIUM"

    else:

        final_priority = "LOW"


    # ========================================================
    # EXECUTIVE DASHBOARD
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Executive Dashboard</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Successfully analyzed {total_reviews} reviews! 🎉"
    )


    # ========================================================
    # METRIC CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📊 TOTAL REVIEWS",
            total_reviews,
            "Customer feedback analyzed"
        )

    with col2:

        st.metric(
            "😊 POSITIVE",
            f"{positive_percent:.1f}%",
            f"{positive_count} positive reviews"
        )

    with col3:

        st.metric(
            "😞 NEGATIVE",
            f"{negative_percent:.1f}%",
            f"{negative_count} negative reviews"
        )

    with col4:

        st.metric(
            "⭐ SATISFACTION",
            f"{satisfaction_score}/100",
            "Overall customer satisfaction"
        )


    # ========================================================
    # BUSINESS HEALTH
    # ========================================================

    st.markdown(
        "### 🏥 Business Health"
    )

    if business_health == "CRITICAL":

        st.error(
            f"🔴 **{business_health}**\n\n"
            f"{health_message}"
        )

    elif business_health == "HIGH":

        st.warning(
            f"🟠 **{business_health}**\n\n"
            f"{health_message}"
        )

    elif business_health == "MEDIUM":

        st.info(
            f"🟡 **{business_health}**\n\n"
            f"{health_message}"
        )

    else:

        st.success(
            f"🟢 **{business_health}**\n\n"
            f"{health_message}"
        )


    # ========================================================
    # CUSTOMER SENTIMENT
    # ========================================================

    st.markdown(
        '<div class="section-title">😊 Customer Sentiment</div>',
        unsafe_allow_html=True
    )

    sentiment_df = pd.DataFrame(
        {
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
        }
    )

    st.bar_chart(
        sentiment_df.set_index(
            "Sentiment"
        ),
        horizontal=True,
        height=250
    )

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


    # ========================================================
    # TOPICS AND PROBLEMS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔎 Customer Topics & Problems'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)


    # ========================================================
    # TOPICS
    # ========================================================

    with col1:

        st.markdown(
            "### 🔍 Most Discussed Topics"
        )

        if topic_counts:

            topic_df = pd.DataFrame(
                list(topic_counts.items()),
                columns=[
                    "Topic",
                    "Mentions"
                ]
            )

            topic_df = topic_df.sort_values(
                "Mentions",
                ascending=True
            )

            st.bar_chart(
                topic_df.set_index(
                    "Topic"
                ),
                horizontal=True,
                height=300
            )

            st.info(
                f"🔍 **Most discussed topic:** "
                f"{main_topic} — "
                f"{main_topic_count} mentions"
            )

        else:

            st.info(
                "No topics detected."
            )


    # ========================================================
    # PROBLEMS
    # ========================================================

    with col2:

        st.markdown(
            "### 🚨 Customer Problems"
        )

        if problem_counts:

            problem_df = pd.DataFrame(
                list(problem_counts.items()),
                columns=[
                    "Problem",
                    "Negative Reviews"
                ]
            )

            problem_df = problem_df.sort_values(
                "Negative Reviews",
                ascending=True
            )

            st.bar_chart(
                problem_df.set_index(
                    "Problem"
                ),
                horizontal=True,
                height=300
            )

            st.warning(
                f"🚨 **Main customer problem:** "
                f"{main_problem} — "
                f"{main_problem_count} negative reviews"
            )

        else:

            st.success(
                "🎉 No major customer problems detected."
            )


    # ========================================================
    # TOPIC INTELLIGENCE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🎯 Topic Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Understand how customers feel about each major topic.'
        '</div>',
        unsafe_allow_html=True
    )

    if topic_sentiment:

        topic_rows = []

        for topic, values in topic_sentiment.items():

            topic_rows.append(
                {
                    "Topic": topic,
                    "Mentions": values["mentions"],
                    "Positive": values["positive"],
                    "Neutral": values["neutral"],
                    "Negative": values["negative"],
                    "Positive %": values["positive_percent"],
                    "Neutral %": values["neutral_percent"],
                    "Negative %": values["negative_percent"]
                }
            )

        topic_sentiment_df = pd.DataFrame(
            topic_rows
        )

        topic_sentiment_df = topic_sentiment_df.sort_values(
            "Negative %",
            ascending=False
        )

        st.dataframe(
            topic_sentiment_df,
            use_container_width=True,
            hide_index=True
        )

        highest_negative_topic = (
            topic_sentiment_df.iloc[0]
        )

        topic_name = (
            highest_negative_topic["Topic"]
        )

        topic_negative_percent = (
            highest_negative_topic["Negative %"]
        )

        topic_negative_count = (
            highest_negative_topic["Negative"]
        )

        st.markdown(
            "### 🚨 Biggest Topic Pain Point"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🔎 TOPIC",
                topic_name
            )

        with col2:

            st.metric(
                "😞 NEGATIVE REVIEWS",
                int(topic_negative_count)
            )

        with col3:

            st.metric(
                "📉 NEGATIVE SENTIMENT",
                f"{topic_negative_percent:.1f}%"
            )

        if topic_negative_percent >= 60:

            st.error(
                f"🔴 **{topic_name} requires immediate attention.** "
                f"{topic_negative_percent:.1f}% of reviews mentioning "
                f"this topic are negative."
            )

        elif topic_negative_percent >= 40:

            st.warning(
                f"🟠 **{topic_name} is a high-priority issue.** "
                f"{topic_negative_percent:.1f}% of reviews mentioning "
                f"this topic are negative."
            )

        elif topic_negative_percent >= 20:

            st.info(
                f"🟡 **{topic_name} needs monitoring.** "
                f"{topic_negative_percent:.1f}% of reviews mentioning "
                f"this topic are negative."
            )

        else:

            st.success(
                f"🟢 **{topic_name} is generally healthy.** "
                f"Only {topic_negative_percent:.1f}% of reviews mentioning "
                f"this topic are negative."
            )

    else:

        st.info(
            "No topic-level sentiment information is available."
        )


    # ========================================================
    # PROBLEM SEVERITY & PRIORITY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🚨 Problem Severity & Priority'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Measure how serious each customer problem is and identify '
        'which issue should be addressed first.'
        '</div>',
        unsafe_allow_html=True
    )

    if problem_severity:

        severity_rows = []

        for problem, values in problem_severity.items():

            severity_rows.append(
                {
                    "Problem": problem,
                    "Negative Reviews": values[
                        "negative_reviews"
                    ],
                    "Negative Share %": values[
                        "negative_share"
                    ],
                    "Review Frequency %": values[
                        "review_frequency"
                    ],
                    "Severity Score": values[
                        "severity_score"
                    ],
                    "Priority": values[
                        "priority"
                    ]
                }
            )

        severity_df = pd.DataFrame(
            severity_rows
        )

        severity_df = severity_df.sort_values(
            "Severity Score",
            ascending=False
        )

        st.dataframe(
            severity_df,
            use_container_width=True,
            hide_index=True
        )

        if highest_severity_problem:

            severity_problem = (
                highest_severity_problem[
                    "problem"
                ]
            )

            severity_score = (
                highest_severity_problem[
                    "severity_score"
                ]
            )

            severity_negative_count = (
                highest_severity_problem[
                    "negative_reviews"
                ]
            )

            severity_negative_share = (
                highest_severity_problem[
                    "negative_share"
                ]
            )

            severity_priority = (
                highest_severity_problem[
                    "priority"
                ]
            )

            st.markdown(
                "### 🏆 Highest Priority Problem"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "🚨 PROBLEM",
                    severity_problem
                )

            with col2:

                st.metric(
                    "😞 NEGATIVE REVIEWS",
                    severity_negative_count
                )

            with col3:

                st.metric(
                    "🎯 SEVERITY SCORE",
                    f"{severity_score:.1f}/100"
                )

            with col4:

                st.metric(
                    "⚡ PRIORITY",
                    severity_priority
                )

            if severity_priority == "CRITICAL":

                st.error(
                    f"🔴 **{severity_problem} requires immediate attention.** "
                    f"It represents {severity_negative_share:.1f}% of all "
                    f"negative problem detections."
                )

            elif severity_priority == "HIGH":

                st.warning(
                    f"🟠 **{severity_problem} is a high-priority problem.** "
                    f"It represents {severity_negative_share:.1f}% of all "
                    f"negative problem detections."
                )

            elif severity_priority == "MEDIUM":

                st.info(
                    f"🟡 **{severity_problem} needs attention.** "
                    f"It represents {severity_negative_share:.1f}% of all "
                    f"negative problem detections."
                )

            else:

                st.success(
                    f"🟢 **{severity_problem} is currently low priority.** "
                    f"Continue monitoring customer feedback."
                )

    else:

        st.success(
            "🎉 No customer problems were detected, so there is no "
            "problem severity score to calculate."
        )


    # ========================================================
    # ROOT CAUSE ANALYSIS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🔍 Root Cause Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Identify the likely reasons behind major customer problems '
        'using evidence found in customer reviews.'
        '</div>',
        unsafe_allow_html=True
    )

    if highest_priority_root_cause:

        problem = highest_priority_root_cause.get(
            "problem",
            "Unknown"
        )

        priority = highest_priority_root_cause.get(
            "priority",
            "LOW"
        )

        severity_score = highest_priority_root_cause.get(
            "severity_score",
            0
        )

        root_cause = highest_priority_root_cause.get(
            "root_cause"
        )

        st.markdown(
            "### 🧠 Highest Priority Root Cause"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🚨 PROBLEM",
                problem
            )

        with col2:

            st.metric(
                "⚡ PRIORITY",
                priority
            )

        with col3:

            st.metric(
                "🎯 SEVERITY SCORE",
                f"{severity_score:.1f}/100"
            )

        if root_cause:

            cause_name = root_cause.get(
                "cause",
                "Unknown"
            )

            evidence_count = root_cause.get(
                "evidence_count",
                0
            )

            st.markdown(
                "### 🔍 Most Likely Root Cause"
            )

            st.info(
                f"🧠 **{cause_name}**"
            )

            if evidence_count > 0:

                st.caption(
                    f"Evidence found in "
                    f"{evidence_count} customer review(s)."
                )

            else:

                st.caption(
                    "The system could not find enough specific evidence "
                    "to determine a strong root cause."
                )


    if root_cause_analysis:

        st.markdown(
            "### 📊 Complete Root Cause Intelligence"
        )

        for item in root_cause_analysis:

            problem = item.get(
                "problem",
                "Unknown"
            )

            priority = item.get(
                "priority",
                "LOW"
            )

            negative_reviews = item.get(
                "negative_reviews",
                0
            )

            root_causes = item.get(
                "root_causes",
                []
            )

            example_reviews = item.get(
                "example_reviews",
                []
            )

            with st.expander(
                f"🚨 {problem} — {priority} Priority"
            ):

                st.metric(
                    "Negative Reviews",
                    negative_reviews
                )

                st.markdown(
                    "#### 🧠 Likely Root Causes"
                )

                for cause_item in root_causes:

                    cause = cause_item.get(
                        "cause",
                        "Unknown"
                    )

                    evidence = cause_item.get(
                        "evidence_count",
                        0
                    )

                    st.write(
                        f"• **{cause}** "
                        f"({evidence} evidence matches)"
                    )

                if example_reviews:

                    st.markdown(
                        "#### 📝 Customer Evidence"
                    )

                    for review_text in example_reviews:

                        st.info(
                            f'"{review_text}"'
                        )

    elif not highest_priority_root_cause:

        st.success(
            "🎉 No major customer problems were found "
            "for root cause analysis."
        )


    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🧠 Executive Summary'
        '</div>',
        unsafe_allow_html=True
    )

    summary = generate_executive_summary(
        positive_percent,
        negative_percent,
        topic_counts
    )

    st.info(
        summary
    )

    business_insight = generate_business_insight(
        negative_percent
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


    # ========================================================
    # CUSTOMER INTELLIGENCE
    # ========================================================

    customer_intelligence = generate_customer_intelligence(
        total_reviews,
        positive_count,
        neutral_count,
        negative_count,
        positive_percent,
        negative_percent,
        topic_counts,
        problem_counts
    )


    # ========================================================
    # AI BUSINESS INSIGHTS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🤖 AI-Powered Business Insights'
        '</div>',
        unsafe_allow_html=True
    )

    ai_insights = customer_intelligence.get(
        "ai_insights",
        []
    )

    if ai_insights:

        st.info(
            "🧠 **REAL AI ANALYSIS**"
        )

        for insight in ai_insights:

            st.markdown(
                insight
            )

            st.divider()

    else:

        st.info(
            "No AI insights available."
        )


    # ========================================================
    # CUSTOMER ACTION CENTER
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🎯 Customer Action Center'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Convert customer feedback into specific business actions.'
        '</div>',
        unsafe_allow_html=True
    )

    action_plan = customer_intelligence.get(
        "action_plan",
        []
    )

    highest_priority_action = (
        customer_intelligence.get(
            "highest_priority_action"
        )
    )


    # ========================================================
    # HIGHEST PRIORITY ACTION
    # ========================================================

    if highest_priority_action:

        priority = highest_priority_action.get(
            "priority",
            "LOW"
        )

        problem = highest_priority_action.get(
            "problem",
            "Unknown"
        )

        action = highest_priority_action.get(
            "action",
            "Investigate the issue."
        )

        impact = highest_priority_action.get(
            "impact",
            "Improving this issue can improve customer experience."
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

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🚨 MAIN PROBLEM",
                problem
            )

        with col2:

            st.metric(
                "🎯 PRIORITY",
                priority
            )

        st.markdown(
            "### 💡 Recommended Action"
        )

        st.info(
            action
        )

        st.markdown(
            "### 📈 Expected Business Impact"
        )

        st.success(
            impact
        )


    # ========================================================
    # COMPLETE ACTION PLAN
    # ========================================================

    st.markdown(
        "### 📋 Complete Action Plan"
    )

    if action_plan:

        for index, action_item in enumerate(
            action_plan,
            start=1
        ):

            if isinstance(
                action_item,
                str
            ):

                with st.expander(
                    f"{index}. Action"
                ):

                    st.write(
                        action_item
                    )

                continue

            priority = action_item.get(
                "priority",
                "LOW"
            )

            problem = action_item.get(
                "problem",
                "Unknown"
            )

            count = action_item.get(
                "count",
                0
            )

            percentage = action_item.get(
                "percentage",
                0
            )

            action = action_item.get(
                "action",
                ""
            )

            impact = action_item.get(
                "impact",
                ""
            )

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


    # ========================================================
    # BUSINESS DECISION ENGINE
    # ========================================================

    business_decision = generate_business_decision_engine(
        problem_counts=problem_counts,
        problem_severity=problem_severity,
        root_cause_intelligence=root_cause_intelligence,
        trend_intelligence=trend_intelligence,
        action_plan=action_plan,
        total_reviews=total_reviews,
        negative_percent=negative_percent
    )

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🧭 Business Decision Engine'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Convert customer evidence into one prioritized business decision: '
        'Problem → Root Cause → Priority → Action → Expected Impact.'
        '</div>',
        unsafe_allow_html=True
    )

    decision_status = business_decision.get(
        "status",
        "MONITOR"
    )

    decision_priority = business_decision.get(
        "priority",
        "LOW"
    )

    decision_confidence = business_decision.get(
        "decision_confidence",
        0
    )

    if decision_status == "ACT NOW":

        st.error(
            f"🔴 **{decision_status}** — "
            "Immediate business intervention recommended."
        )

    elif decision_status == "ACT SOON":

        st.warning(
            f"🟠 **{decision_status}** — "
            "Address this issue in the next improvement cycle."
        )

    elif decision_status == "PLAN":

        st.info(
            f"🟡 **{decision_status}** — "
            "Add this issue to the improvement plan."
        )

    else:

        st.success(
            f"🟢 **{decision_status}** — "
            "Continue monitoring customer feedback."
        )


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🚨 PRIORITY",
            decision_priority
        )

    with col2:

        decision_severity_score = business_decision.get(
            "severity_score",
            0
        )

        st.metric(
            "🎯 SEVERITY",
            f"{decision_severity_score:.1f}/100"
        )

    with col3:

        st.metric(
            "🧠 CONFIDENCE",
            f"{decision_confidence}%"
        )

    with col4:

        related_occurrences = business_decision.get(
            "related_occurrences",
            0
        )

        st.metric(
            "🔁 RELATED OCCURRENCES",
            related_occurrences
        )


    # ========================================================
    # DECISION CHAIN
    # ========================================================

    st.markdown(
        "### 🔗 Decision Chain"
    )

    chain = business_decision.get(
        "decision_chain",
        []
    )

    if len(chain) >= 5:

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:

            st.info(
                f"**1. Problem**\n\n{chain[0]}"
            )

        with c2:

            st.info(
                f"**2. Root Cause**\n\n{chain[1]}"
            )

        with c3:

            st.info(
                f"**3. Priority**\n\n{chain[2]}"
            )

        with c4:

            st.info(
                f"**4. Recommended Action**\n\n{chain[3]}"
            )

        with c5:

            st.success(
                f"**5. Expected Impact**\n\n{chain[4]}"
            )


    # ========================================================
    # DECISION RATIONALE
    # ========================================================

    st.markdown(
        "### 🧠 Decision Rationale"
    )

    st.write(
        business_decision.get(
            "reason",
            "No rationale available."
        )
    )

    decision_evidence = business_decision.get(
        "evidence",
        0
    )

    decision_trend = business_decision.get(
        "trend",
        "NO DATA"
    )

    st.caption(
        f"Root-cause evidence: "
        f"{decision_evidence} review match(es) • "
        f"Sentiment trend: "
        f"{decision_trend}"
    )


    # ========================================================
    # ADVANCED TREND & PATTERN INTELLIGENCE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📈 Advanced Trend & Pattern Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Detect recurring issues, sentiment direction, '
        'topic–problem relationships, '
        'and important customer patterns.'
        '</div>',
        unsafe_allow_html=True
    )

    trend_name = sentiment_trend_analysis.get(
        "trend",
        "NO DATA"
    )

    trend_direction = sentiment_trend_analysis.get(
        "direction",
        "No trend available."
    )

    first_half_average = sentiment_trend_analysis.get(
        "first_half_average",
        0
    )

    second_half_average = sentiment_trend_analysis.get(
        "second_half_average",
        0
    )

    trend_change = sentiment_trend_analysis.get(
        "change",
        0
    )


    # ========================================================
    # SENTIMENT DIRECTION
    # ========================================================

    st.markdown(
        "### 📊 Sentiment Direction"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📈 TREND",
            trend_name
        )

    with col2:

        st.metric(
            "🔹 EARLIER AVERAGE",
            f"{first_half_average:.2f}"
        )

    with col3:

        st.metric(
            "🔹 LATER AVERAGE",
            f"{second_half_average:.2f}"
        )

    with col4:

        st.metric(
            "↕️ CHANGE",
            f"{trend_change:+.2f}"
        )


    if trend_name == "WORSENING":

        st.error(
            f"📉 **{trend_direction}**"
        )

    elif trend_name == "IMPROVING":

        st.success(
            f"📈 **{trend_direction}**"
        )

    elif trend_name == "STABLE":

        st.info(
            f"➖ **{trend_direction}**"
        )

    else:

        st.info(
            trend_direction
        )


    # ========================================================
    # RECURRING PROBLEMS
    # ========================================================

    st.markdown(
        "### 🔁 Recurring Problems"
    )

    if recurring_problems:

        recurring_rows = []

        for item in recurring_problems:

            if isinstance(
                item,
                dict
            ):

                recurring_rows.append(
                    {
                        "Problem": item.get(
                            "problem",
                            "Unknown"
                        ),
                        "Occurrences": item.get(
                            "count",
                            0
                        ),
                        "Review Frequency %": item.get(
                            "percentage",
                            0
                        ),
                        "Pattern": item.get(
                            "recurrence",
                            "OCCASIONAL"
                        )
                    }
                )

        if recurring_rows:

            recurring_df = pd.DataFrame(
                recurring_rows
            )

            st.dataframe(
                recurring_df,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.success(
            "🎉 No recurring customer problems were detected."
        )


    # ========================================================
    # TOPIC–PROBLEM RELATIONSHIPS
    # ========================================================

    st.markdown(
        "### 🔗 Topic–Problem Relationships"
    )

    if topic_problem_relationships:

        relationship_rows = []

        for item in topic_problem_relationships[:10]:

            if isinstance(
                item,
                dict
            ):

                relationship_rows.append(
                    {
                        "Topic": item.get(
                            "topic",
                            "Unknown"
                        ),
                        "Problem": item.get(
                            "problem",
                            "Unknown"
                        ),
                        "Co-occurrences": item.get(
                            "count",
                            0
                        )
                    }
                )

        if relationship_rows:

            relationship_df = pd.DataFrame(
                relationship_rows
            )

            st.dataframe(
                relationship_df,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.info(
            "No strong topic–problem relationships were detected."
        )


    # ========================================================
    # PATTERN ALERTS
    # ========================================================

    st.markdown(
        "### 🚨 Pattern Alerts"
    )

    if pattern_alerts:

        for alert in pattern_alerts:

            if not isinstance(
                alert,
                dict
            ):

                st.info(
                    str(alert)
                )

                continue

            level = alert.get(
                "level",
                "MEDIUM"
            )

            title = alert.get(
                "title",
                "Pattern Alert"
            )

            message = alert.get(
                "message",
                ""
            )

            alert_text = (
                f"**{title}**\n\n"
                f"{message}"
            )

            if level == "CRITICAL":

                st.error(
                    f"🔴 {alert_text}"
                )

            elif level == "HIGH":

                st.warning(
                    f"🟠 {alert_text}"
                )

            elif level == "POSITIVE":

                st.success(
                    f"🟢 {alert_text}"
                )

            else:

                st.info(
                    f"🟡 {alert_text}"
                )

    else:

        st.success(
            "🎉 No major pattern alerts were generated."
        )


    # ========================================================
    # BUSINESS DECISION SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📊 Business Decision Summary'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'A consolidated view of customer experience, '
        'business health and recommended action.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏥 BUSINESS HEALTH",
            business_health
        )

    with col2:

        st.metric(
            "⭐ SATISFACTION",
            f"{satisfaction_score}/100"
        )

    with col3:

        st.metric(
            "🔍 TOPIC",
            main_topic,
            f"{main_topic_count} mentions"
        )

    with col4:

        st.metric(
            "🚨 MAIN PROBLEM",
            main_problem,
            f"{main_problem_count} negative reviews"
        )


    # ========================================================
    # FINAL BUSINESS ACTION
    # ========================================================

    st.markdown(
        "### 🎯 Final Business Action"
    )

    st.write(
        f"**Priority:** {final_priority}"
    )

    if priority_recommendation:

        st.info(
            f"💡 **Recommended Action:** "
            f"{priority_recommendation}"
        )

    if highest_priority_action:

        final_impact = highest_priority_action.get(
            "impact",
            "Improving the identified issue can improve customer satisfaction."
        )

        st.success(
            f"📈 **Expected Business Impact:** "
            f"{final_impact}"
        )


    # ========================================================
    # SENTIMENT TREND
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📈 Sentiment Trend'
        '</div>',
        unsafe_allow_html=True
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
            trend_data,
            height=350
        )

        st.caption(
            "Sentiment score progression across "
            "the uploaded customer reviews."
        )

    else:

        st.info(
            "At least two reviews are required "
            "to display a sentiment trend."
        )


    # ========================================================
    # DETAILED REVIEW ANALYSIS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📋 Detailed Review Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DOWNLOAD ANALYZED CSV
    # ========================================================

    csv_data = data.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Analysis CSV",
        data=csv_data,
        file_name="review_analysis.csv",
        mime="text/csv"
    )


    # ========================================================
    # AI BUSINESS REPORT GENERATOR
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📄 AI Business Report Generator'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Generate a professional business report from the complete '
        'customer review intelligence analysis.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # REPORT GENERATION FUNCTION
    # ========================================================

    def create_business_report():

        try:

            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import (
                getSampleStyleSheet,
                ParagraphStyle
            )
            from reportlab.lib.enums import TA_CENTER
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle
            )
            from reportlab.lib.units import inch

            buffer = BytesIO()

            document = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                "ReportTitle",
                parent=styles["Title"],
                fontSize=22,
                leading=28,
                alignment=TA_CENTER,
                spaceAfter=18
            )

            subtitle_style = ParagraphStyle(
                "ReportSubtitle",
                parent=styles["BodyText"],
                fontSize=11,
                leading=15,
                alignment=TA_CENTER,
                spaceAfter=20
            )

            heading_style = ParagraphStyle(
                "ReportHeading",
                parent=styles["Heading2"],
                fontSize=15,
                leading=20,
                spaceBefore=14,
                spaceAfter=8
            )

            normal_style = ParagraphStyle(
                "ReportNormal",
                parent=styles["BodyText"],
                fontSize=10,
                leading=15,
                spaceAfter=7
            )

            story = []


            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "Review Intelligence",
                    title_style
                )
            )

            story.append(
                Paragraph(
                    "AI-Powered Customer Experience & "
                    "Business Decision Report",
                    subtitle_style
                )
            )


            # ------------------------------------------------
            # EXECUTIVE OVERVIEW
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "1. Executive Overview",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"This report analyzes <b>{total_reviews}</b> "
                    f"customer reviews to identify customer sentiment, "
                    f"major topics, customer problems, root causes, "
                    f"business priorities and recommended actions.",
                    normal_style
                )
            )


            # ------------------------------------------------
            # BUSINESS HEALTH
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "2. Business Health",
                    heading_style
                )
            )

            health_data = [
                ["Metric", "Value"],
                [
                    "Total Reviews",
                    str(total_reviews)
                ],
                [
                    "Positive Reviews",
                    f"{positive_count} "
                    f"({positive_percent:.1f}%)"
                ],
                [
                    "Neutral Reviews",
                    f"{neutral_count} "
                    f"({neutral_percent:.1f}%)"
                ],
                [
                    "Negative Reviews",
                    f"{negative_count} "
                    f"({negative_percent:.1f}%)"
                ],
                [
                    "Customer Satisfaction",
                    f"{satisfaction_score}/100"
                ],
                [
                    "Business Health",
                    business_health
                ]
            ]

            health_table = Table(
                health_data,
                colWidths=[
                    2.5 * inch,
                    3.5 * inch
                ]
            )

            health_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#334155")
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTNAME",
                        (0, 1),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ])
            )

            story.append(
                health_table
            )


            # ------------------------------------------------
            # CUSTOMER TOPICS
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "3. Customer Topics",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Most Discussed Topic:</b> "
                    f"{main_topic} "
                    f"({main_topic_count} mentions)",
                    normal_style
                )
            )

            if topic_counts:

                topic_text = ", ".join(
                    [
                        f"{topic}: {count}"
                        for topic, count in sorted(
                            topic_counts.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )
                    ]
                )

                story.append(
                    Paragraph(
                        f"<b>Topic Distribution:</b> "
                        f"{topic_text}",
                        normal_style
                    )
                )


            # ------------------------------------------------
            # CUSTOMER PROBLEMS
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "4. Customer Problems",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Main Customer Problem:</b> "
                    f"{main_problem}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Detected Negative Reviews:</b> "
                    f"{main_problem_count}",
                    normal_style
                )
            )


            # ------------------------------------------------
            # ROOT CAUSE
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "5. Root Cause Intelligence",
                    heading_style
                )
            )

            report_root_cause = business_decision.get(
                "root_cause",
                "Insufficient evidence to identify "
                "a specific root cause."
            )

            report_evidence = business_decision.get(
                "evidence",
                0
            )

            story.append(
                Paragraph(
                    f"<b>Likely Root Cause:</b> "
                    f"{report_root_cause}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Supporting Evidence:</b> "
                    f"{report_evidence} review match(es)",
                    normal_style
                )
            )


            # ------------------------------------------------
            # BUSINESS DECISION
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "6. Business Decision",
                    heading_style
                )
            )

            report_status = business_decision.get(
                "status",
                "MONITOR"
            )

            report_priority = business_decision.get(
                "priority",
                "LOW"
            )

            report_severity_score = business_decision.get(
                "severity_score",
                0
            )

            report_decision_confidence = business_decision.get(
                "decision_confidence",
                0
            )

            report_related_occurrences = business_decision.get(
                "related_occurrences",
                0
            )

            report_trend = business_decision.get(
                "trend",
                "NO DATA"
            )

            decision_data = [
                ["Decision Metric", "Result"],
                [
                    "Decision Status",
                    str(report_status)
                ],
                [
                    "Priority",
                    str(report_priority)
                ],
                [
                    "Severity Score",
                    f"{report_severity_score:.1f}/100"
                ],
                [
                    "Decision Confidence",
                    f"{report_decision_confidence}%"
                ],
                [
                    "Related Occurrences",
                    str(report_related_occurrences)
                ],
                [
                    "Sentiment Trend",
                    str(report_trend)
                ]
            ]

            decision_table = Table(
                decision_data,
                colWidths=[
                    2.5 * inch,
                    3.5 * inch
                ]
            )

            decision_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#334155")
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTNAME",
                        (0, 1),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    )
                ])
            )

            story.append(
                decision_table
            )


            # ------------------------------------------------
            # RECOMMENDED ACTION
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "7. Recommended Business Action",
                    heading_style
                )
            )

            recommended_action = business_decision.get(
                "recommended_action",
                "Continue monitoring customer feedback."
            )

            expected_impact = business_decision.get(
                "expected_impact",
                "Improving the identified issue can improve "
                "customer experience."
            )

            story.append(
                Paragraph(
                    f"<b>Recommended Action:</b> "
                    f"{recommended_action}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Expected Business Impact:</b> "
                    f"{expected_impact}",
                    normal_style
                )
            )


            # ------------------------------------------------
            # DECISION RATIONALE
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "8. Decision Rationale",
                    heading_style
                )
            )

            decision_reason = business_decision.get(
                "reason",
                "No rationale available."
            )

            story.append(
                Paragraph(
                    str(decision_reason),
                    normal_style
                )
            )


            # ------------------------------------------------
            # SENTIMENT TREND
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "9. Sentiment Trend",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Trend:</b> {trend_name}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Earlier Average:</b> "
                    f"{first_half_average:.2f}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Later Average:</b> "
                    f"{second_half_average:.2f}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Change:</b> "
                    f"{trend_change:+.2f}",
                    normal_style
                )
            )


            # ------------------------------------------------
            # EXECUTIVE SUMMARY
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "10. Executive Summary",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    str(summary),
                    normal_style
                )
            )


            # ------------------------------------------------
            # FINAL BUSINESS RECOMMENDATION
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "11. Final Business Recommendation",
                    heading_style
                )
            )

            final_problem = business_decision.get(
                "problem",
                main_problem
            )

            final_decision_priority = business_decision.get(
                "priority",
                final_priority
            )

            story.append(
                Paragraph(
                    f"The organization should prioritize "
                    f"<b>{final_problem}</b>. "
                    f"The recommended priority is "
                    f"<b>{final_decision_priority}</b>. "
                    f"The system recommends: "
                    f"<b>{recommended_action}</b>",
                    normal_style
                )
            )


            # ------------------------------------------------
            # FOOTER
            # ------------------------------------------------

            story.append(
                Spacer(
                    1,
                    20
                )
            )

            story.append(
                Paragraph(
                    "Generated by Review Intelligence — "
                    "AI-powered Customer Experience & "
                    "Business Decision Platform",
                    ParagraphStyle(
                        "ReportFooter",
                        parent=styles["BodyText"],
                        fontSize=8,
                        leading=11,
                        alignment=TA_CENTER
                    )
                )
            )


            # ------------------------------------------------
            # BUILD PDF
            # ------------------------------------------------

            document.build(
                story
            )

            buffer.seek(0)

            return buffer.getvalue()

        except Exception as error:

            st.error(
                f"Unable to generate business report: {error}"
            )

            return None


    # ========================================================
    # GENERATE REPORT BUTTON
    # ========================================================

    if st.button(
        "📄 Generate Business Report",
        key="generate_business_report"
    ):

        with st.spinner(
            "Generating your business report..."
        ):

            pdf_data = create_business_report()

        if pdf_data:

            st.success(
                "✅ Business report generated successfully!"
            )

            st.download_button(
                label="⬇️ Download Business Report (PDF)",
                data=pdf_data,
                file_name=(
                    "review_intelligence_business_report.pdf"
                ),
                mime="application/pdf",
                key="download_business_report"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="dashboard-footer">
        🔍 Review Intelligence •
        Customer Experience & Business Decision Platform
    </div>
    """,
    unsafe_allow_html=True
)
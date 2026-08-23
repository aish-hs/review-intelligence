# 📊 Review Intelligence

### AI-Powered Customer Review Analysis & Business Decision Intelligence

Review Intelligence is a Python and Streamlit-based application that transforms customer reviews into actionable business insights.

It analyzes customer feedback using **sentiment analysis, topic detection, problem identification, severity analysis, root-cause intelligence, recommendations, and business insights**.

The goal is to help businesses understand **what customers like, what they dislike, what problems they are experiencing, and what actions should be taken next.**

---

## 🚀 Live Demo

Try the deployed application:

https://review-intelligence-drxtcdtnh2r44dbrbjwg5o.streamlit.app/

---

## ✨ Features

### 📝 Single Review Analysis

Enter an individual customer review and instantly receive:

* Sentiment classification
* Sentiment score
* Detected topics
* Customer problems
* Recommendations

### 📊 Review Dashboard

Analyze an entire CSV dataset and view:

* Total reviews
* Positive reviews
* Negative reviews
* Neutral reviews
* Overall customer satisfaction
* Business health
* Sentiment distribution
* Sentiment trends

### 🎯 Topic Intelligence

Identifies the most frequently discussed areas in customer reviews, such as:

* Product quality
* Delivery
* Pricing
* Customer service
* Packaging
* Product availability

The application also analyzes the sentiment associated with each topic.

### 🚨 Customer Problem Detection

Automatically identifies common customer problems and categorizes their severity.

The dashboard provides:

* Problem frequency
* Problem severity
* Highest-severity problem
* Negative review impact

### 🔍 Root Cause Intelligence

The system analyzes customer complaints to identify possible root causes behind recurring problems.

This helps businesses move beyond simply identifying complaints and understand **why the problem may be occurring.**

### 💡 Priority Recommendations

The application generates business recommendations based on detected customer problems and their severity.

Recommendations help businesses determine which issues should be addressed first.

### 🧠 Business Intelligence

The dashboard converts customer feedback into higher-level business insights, including:

* Executive summary
* Business health
* Customer satisfaction
* Priority issues
* Business recommendations
* Customer intelligence

---

## 🛠️ Technologies Used

| Technology      | Purpose                      |
| --------------- | ---------------------------- |
| Python          | Core programming language    |
| Streamlit       | Interactive web dashboard    |
| Pandas          | Data processing and analysis |
| NLP             | Customer review analysis     |
| Git             | Version control              |
| GitHub          | Source code management       |
| Streamlit Cloud | Application deployment       |

---

## 🏗️ Project Architecture

```text
Customer Reviews CSV
        │
        ▼
   Data Processing
        │
        ▼
  Sentiment Analysis
        │
        ▼
   Topic Detection
        │
        ▼
 Problem Identification
        │
        ▼
 Severity Analysis
        │
        ▼
 Root Cause Intelligence
        │
        ▼
 Recommendations
        │
        ▼
 Business Intelligence
        │
        ▼
 Streamlit Dashboard
```

---

## 📁 Project Structure

```text
review-intelligence/
│
├── app.py
├── main.py
│
├── sentiment.py
├── topics.py
├── recommendations.py
├── data_processor.py
├── root_cause.py
├── action_center.py
├── ai_insights.py
├── business_summary.py
├── decision_engine.py
├── executive_report.py
├── llm_service.py
├── trend_analysis.py
│
├── reviews.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── test files
```

---

## 🔄 How It Works

### 1. Upload Customer Reviews

The user uploads a CSV file containing customer reviews.

### 2. Analyze Reviews

The application processes each review and performs:

* Sentiment analysis
* Topic detection
* Problem detection
* Severity analysis

### 3. Identify Customer Issues

The system identifies recurring complaints and determines which problems require the most attention.

### 4. Generate Business Insights

The analyzed data is converted into:

* Customer satisfaction metrics
* Topic intelligence
* Problem intelligence
* Root-cause insights
* Business recommendations

### 5. Display Results

All insights are presented through an interactive Streamlit dashboard.

---

## 📈 Example Dashboard Insights

The dashboard can provide insights such as:

```text
Positive Reviews:       66.7%
Negative Reviews:       33.3%
Customer Satisfaction:  67/100
```

It can also identify:

* Most mentioned topics
* Most common customer problems
* Highest severity problem
* Topic-level sentiment
* Priority recommendations
* Overall business health

---

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/aish-hs/review-intelligence.git
```

Move into the project directory:

```bash
cd review-intelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📄 Input Dataset

The application accepts customer review data in CSV format.

Example:

```text
review
"The product quality is excellent and delivery was fast."
"The product arrived damaged and customer support was not helpful."
"The price is good but packaging needs improvement."
```

---

## 🔐 Environment Variables

If API-based AI functionality is enabled, API credentials should be stored in a `.env` file.

Example:

```text
GOOGLE_API_KEY=your_api_key_here
```

**Never upload ****`.env`**** or API keys to GitHub.**

The project uses `.gitignore` to prevent sensitive files from being committed.

---

## 🧪 Testing

The project contains test files for validating different components of the application.

Example:

```bash
python test_ai_insights.py
```

---

## 🎯 Project Goals

Review Intelligence was designed to solve a common business problem:

> Businesses receive large amounts of customer feedback but often struggle to convert that feedback into actionable decisions.

This project attempts to bridge that gap by transforming unstructured customer reviews into structured business intelligence.

---

## 🔮 Future Improvements

Potential future enhancements include:

* 🤖 Advanced LLM-powered review analysis
* 📡 Real-time review collection
* 🛒 E-commerce platform integrations
* 📱 Mobile-friendly dashboard
* 💬 AI business intelligence chatbot
* 🎙️ Voice feedback analysis
* 📈 Advanced predictive analytics
* 🔔 Automated business alerts
* 📊 Historical trend forecasting
* 🌐 Multi-platform review aggregation

---

## 👩‍💻 Author

**Aishwarya H S**

Information Science  Engineering Student

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**Review Intelligence — Turning customer feedback into business decisions.**

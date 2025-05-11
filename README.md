# 🗞️ News Sentiment Analysis – BIU Assignment (Part 2)

This repository contains the implementation of **Part 2: Web Scraping & Sentiment Analysis** as part of the **BIU Team assignment for Guidance Tamil Nadu**.

---

## 🎯 Objective

To extract, analyze, and classify recent news headlines related to the **electronics, semiconductors, and manufacturing** sectors using NLP-based sentiment analysis techniques. The aim is to provide quick insights into current media narratives relevant to industrial development and investment.

---

## 📰 Data Collection

- **Method**: RSS Feed-based Web Scraping
- **Sources**: Publicly accessible business news RSS feeds
- **Criteria**: Headlines relevant to business, manufacturing, semiconductors, and electronics sectors
- **Data Points Extracted**:
  - **Headline Title**
  - **URL**
  - **Timestamp**
  - **Country Mentioned** (if available)

---

## 🤖 Sentiment Analysis

- **Tool Used**: [VADER (Valence Aware Dictionary for sEntiment Reasoning)](https://github.com/cjhutto/vaderSentiment)
- **Language Processing**: English
- **Classification Labels**:
  - ✅ **Positive**
  - ⚪ **Neutral**
  - ❌ **Negative**

VADER is particularly suited for short-form content like news headlines and tweets, making it ideal for this task.

---

## 📊 Visualization & Dashboard

- **Platform**: [Streamlit](https://streamlit.io/)
- **Features**:
  - Bar chart showing sentiment distribution
  - List of headlines by sentiment category
  - Intuitive and lightweight dashboard UI

---

## 📂 Repository Structure

```

News\_sentiment\_Analysis/
│
├── news\_sentiment\_analysis.ipynb      # Final working notebook
├── news\_sentiment\_trial.ipynb         # Trial/testing notebook
├── sentiment\_data.csv                 # Output dataset with sentiment labels
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation

````

---

## ✅ Tasks & Workflow

### 1️⃣ Web Scraping

- Used the `feedparser` library to extract headlines from legal, publicly available RSS feeds.
- Stored extracted data in structured format using `pandas`.

### 2️⃣ Sentiment Scoring

- Cleaned and processed text for sentiment analysis.
- Applied VADER’s polarity scoring.
- Assigned sentiment category based on compound score thresholds.

### 3️⃣ Visualization

- Aggregated sentiment counts using `pandas`.
- Plotted sentiment distribution using `matplotlib` and `seaborn`.
- Built a Streamlit dashboard for interactive exploration.

---

## 🚀 Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/arunvithyasegar/News_sentiment_Analysis.git
   cd News_sentiment_Analysis
````

2. **Create a Virtual Environment (optional)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:

   ```bash
   streamlit run news_sentiment_analysis.ipynb
   ```

---

## 📈 Sample Output

* 🧾 **Headline**: “India ramps up semiconductor push with new FDI policy”
* 🏷️ **Sentiment**: Positive
* 📍 **Country Mentioned**: India

Example visualizations:

* Bar chart showing distribution of positive, neutral, and negative headlines
* Headline table filtered by sentiment

---

## 🛠️ Tools & Libraries

* **Python**
* `feedparser` – RSS feed extraction
* `nltk`, `vaderSentiment` – NLP and sentiment analysis
* `pandas` – Data manipulation
* `matplotlib`, `seaborn` – Visualization
* `streamlit` – Dashboard and UI

---

## 🌐 Live Dashboard

Explore the sentiment breakdown of current business headlines:

🔗 [News Sentiment Dashboard](https://newssentimentanalysis.streamlit.app/)

---

## 📄 License

This project is created exclusively for the BIU Assignment at [Guidance Tamil Nadu](https://investingintamilnadu.com/DIGIGOV/TN-pages/guidance.jsp?pagedisp=static) and is not intended for commercial or production use.

---

## 👨‍💻 Author

**Arun Vithyasegar**
[LinkedIn](https://www.linkedin.com/in/arunvithyasegar) | [GitHub](https://github.com/arunvithyasegar)

---

> *Note*: This project analyzes publicly available content from RSS feeds. No proprietary or paid APIs were used. VADER is a rule-based sentiment engine designed for social media and news-style text.

```

Let me know if you'd like a version that combines Part 1 and Part 2 into one comprehensive `README.md`, or need help exporting this to PDF or a DOCX format.
```

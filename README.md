Here is the corrected and properly formatted version of your `README.md` file, including syntax highlighting, consistent structure, and fixed markdown rendering issues:

---

```markdown
# News Sentiment Analysis – BIU Assignment (Part 2)

This repository contains the implementation of **Part 2: Web Scraping & Sentiment Analysis** as part of the BIU Team assignment for **Guidance Tamil Nadu**.

---

## 🎯 Objective

To extract and analyze recent news headlines related to the **electronics, semiconductors, and manufacturing** sectors using publicly accessible sources, and classify them by sentiment using Natural Language Processing (NLP) techniques.

---

## ✨ Features

### 🔍 Web Scraping

- Utilized an RSS feed to legally collect 20 business news headlines.
- Extracted the following from each article:
  - **Title**
  - **URL**
  - **Timestamp**
  - **Country Mentioned**

### 💬 Sentiment Analysis

- Sentiment classification performed using **VADER (Valence Aware Dictionary for Sentiment Reasoning)**.
- Headlines categorized as:
  - **Positive**
  - **Neutral**
  - **Negative**

### 📊 Visualization

- Bar chart showing sentiment distribution.
- Interactive, professional dashboard created using **Streamlit**.

---

## 🚀 Live Dashboard

👉 [Click here to view the interactive news sentiment dashboard](https://newssentimentanalysis.streamlit.app/)

---

## 📁 Repository Structure

```

News\_sentiment\_Analysis/
│
├── news\_sentiment\_analysis.ipynb    # Final working solution
├── news\_sentiment\_trial.ipynb       # Trial/testing notebook
├── requirements.txt                 # Required Python packages
├── sentiment\_data.csv               # Output data with sentiment labels
└── README.md                        # Documentation

````

---

## 🛠️ How to Run Locally

1. **Clone the repo**:
   ```bash
   git clone https://github.com/arunvithyasegar/News_sentiment_Analysis.git
   cd News_sentiment_Analysis
````

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the notebook or launch the Streamlit app**:

   ```bash
   streamlit run news_sentiment_analysis.ipynb
   ```

---

## 🧰 Tools Used

* **Python**
* **Feedparser** – For RSS data extraction
* **NLTK & VADER** – For sentiment analysis
* **Pandas** – Data wrangling
* **Matplotlib / Seaborn** – Data visualization
* **Streamlit** – Web app/dashboard development

---

## 📄 License

This project is created strictly for the **BIU Assignment at Guidance Tamil Nadu** and is not intended for commercial or production use.

---

## 👨‍💻 Author

**Arun Vithyasegar**
[LinkedIn](https://www.linkedin.com/in/arunvithyasegar) | [GitHub](https://github.com/arunvithyasegar)

---

```





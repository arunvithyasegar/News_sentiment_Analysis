import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, visualize_sentiment

# Set page configuration
st.set_page_config(
    page_title="News Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #555;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("<div class='main-header'>News Sentiment Analysis Dashboard</div>", unsafe_allow_html=True)
st.markdown("### GUIDANCE – BIU TEAM ASSIGNMENT")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Section",
    ["Home", "News Sentiment Analysis"]
)

# Home Page
if page == "Home":
    st.markdown("<div class='sub-header'>Welcome to the Dashboard</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    This interactive dashboard provides analysis for:
    <ul>
        <li><b>News Sentiment Analysis</b>: Analyzing sentiment of recent news headlines related to electronics, semiconductors, or manufacturing</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Instructions</div>", unsafe_allow_html=True)
    st.markdown("""
    - Use the sidebar to navigate to the News Sentiment Analysis section
    - In the News Sentiment Analysis section, you can:
        - View scraped news headlines
        - See sentiment analysis results
        - Explore sentiment distribution visualizations
    """)
    
    # Sample visualization for the home page
    st.markdown("<div class='section-header'>Dashboard Preview</div>", unsafe_allow_html=True)
    
    st.image("https://miro.medium.com/max/1400/1*Uu0RqBu1CgEfSLUzQEFIHw.png", 
             caption="Sentiment Analysis Visualization")

# News Sentiment Analysis Page
elif page == "News Sentiment Analysis":
    st.markdown("<div class='sub-header'>News Sentiment Analysis</div>", unsafe_allow_html=True)
    
    # Options for news sources
    news_source = st.selectbox(
        "Select News Source",
        ["NewsAPI", "Reuters", "Bloomberg", "Manual Input"]
    )
    
    # Keywords for filtering news
    keywords = st.text_input(
        "Enter keywords for news filtering (comma-separated)",
        value="electronics, semiconductors, manufacturing"
    )
    
    # Number of articles to fetch
    num_articles = st.slider(
        "Number of articles to analyze",
        min_value=5,
        max_value=50,
        value=20
    )
    
    # Button to fetch and analyze news - ADD A UNIQUE KEY HERE
    fetch_button = st.button("Fetch and Analyze News", key="fetch_analyze_button")
    
    if fetch_button:
        with st.spinner("Fetching news and analyzing sentiment..."):
            # Scrape news based on selected source
            if news_source == "Manual Input":
                st.markdown("<div class='section-header'>Enter News Headlines Manually</div>", unsafe_allow_html=True)
                
                # Create a form for manual input
                with st.form("manual_news_form"):
                    manual_news = st.text_area(
                        "Enter news headlines (one per line)",
                        height=200,
                        help="Enter one headline per line. You can add URL, timestamp, and country after the headline, separated by commas."
                    )
                    
                    submit_button = st.form_submit_button("Analyze Entered Headlines")
                
                if submit_button and manual_news:
                    # Process manual input
                    news_data = []
                    for line in manual_news.strip().split('\n'):
                        parts = [part.strip() for part in line.split(',')]
                        title = parts[0]
                        url = parts[1] if len(parts) > 1 else "N/A"
                        timestamp = parts[2] if len(parts) > 2 else "N/A"
                        country = parts[3] if len(parts) > 3 else "N/A"
                        
                        news_data.append({
                            'title': title,
                            'url': url,
                            'timestamp': timestamp,
                            'country': country
                        })
                    
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Display results
                    st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                    
                    # Create a DataFrame for display
                    results_df = pd.DataFrame(sentiment_results)
                    st.dataframe(results_df)
                    
                    # Visualize sentiment distribution
                    st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                    
                    # Create visualization
                    fig = visualize_sentiment(sentiment_results)
                    st.pyplot(fig)
            else:
                # Scrape news from selected source
                news_data = scrape_news(news_source, keywords.split(','), num_articles)
                
                if news_data:
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Display results
                    st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                    
                    # Create a DataFrame for display
                    results_df = pd.DataFrame(sentiment_results)
                    st.dataframe(results_df)
                    
                    # Visualize sentiment distribution
                    st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                    
                    # Create visualization
                    fig = visualize_sentiment(sentiment_results)
                    st.pyplot(fig)
                else:
                    st.error("Failed to fetch news. Please try another source or check your internet connection.")
    
    # Sample data for demonstration - CHANGE THIS CONDITION AND ADD A UNIQUE KEY
    # Instead of checking the button again, use a separate variable
    if not fetch_button:
        st.info("Click the button above to fetch and analyze news headlines.")
        
        st.markdown("<div class='section-header'>Sample Sentiment Analysis</div>", unsafe_allow_html=True)
        
        # Sample sentiment data
        sample_sentiment = {
            'title': [
                "Global chip shortage eases as production ramps up",
                "Electronics manufacturers face supply chain disruptions",
                "New semiconductor plant opens in Taiwan",
                "Tech companies report mixed Q2 earnings",
                "Trade tensions impact electronics exports"
            ],
            'source': ['Reuters', 'Bloomberg', 'TechCrunch', 'CNBC', 'WSJ'],
            'date': ['2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05'],
            'country': ['Global', 'China', 'Taiwan', 'USA', 'Global'],
            'sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative'],
            'score': [0.65, -0.48, 0.72, 0.05, -0.52]
        }
        
        sample_df = pd.DataFrame(sample_sentiment)
        st.dataframe(sample_df)
        
        # Sample visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sentiment_counts = sample_df['sentiment'].value_counts()
        colors = {'Positive': 'green', 'Neutral': 'blue', 'Negative': 'red'}
        
        bars = ax.bar(sentiment_counts.index, sentiment_counts.values, color=[colors[s] for s in sentiment_counts.index])
        
        ax.set_title('Sentiment Distribution of News Headlines')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')
        
        # Add count labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height}', ha='center', va='bottom')
        
        st.pyplot(fig)
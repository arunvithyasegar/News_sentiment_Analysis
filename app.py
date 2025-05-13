import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import time
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, create_sentiment_visualizations

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
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f5f5f5;
        border-radius: 0.5rem;
        font-size: 0.9rem;
        color: #555;
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
    ["Home", "News Sentiment Analysis", "About"]
)

# Home Page
if page == "Home":
    st.markdown("<div class='sub-header'>Welcome to the Real-Time News Dashboard</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    This interactive dashboard provides real-time analysis for:
    <ul>
        <li><b>Live News Sentiment Analysis</b>: Real-time sentiment analysis of latest news headlines related to electronics, semiconductors, or manufacturing</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Instructions</div>", unsafe_allow_html=True)
    st.markdown("""
    - Use the sidebar to navigate to the News Sentiment Analysis section
    - In the News Sentiment Analysis section, you can:
        - View live news headlines as they are published
        - Get instant sentiment analysis results
        - See real-time sentiment distribution visualizations
        - Set up auto-refresh intervals
    """)
    
    # Sample visualization for the home page
    st.markdown("<div class='section-header'>Live Dashboard Preview</div>", unsafe_allow_html=True)
    
    st.image("https://miro.medium.com/max/1400/1*Uu0RqBu1CgEfSLUzQEFIHw.png", 
             caption="Real-Time Sentiment Analysis Visualization")

# News Sentiment Analysis Page
elif page == "News Sentiment Analysis":
    st.markdown("<div class='sub-header'>Business Tech News Sentiment Analysis</div>", unsafe_allow_html=True)
    
    # Default keywords focused on tech and manufacturing
    default_keywords = "electronics, semiconductors, manufacturing, technology"
    keywords = st.text_input(
        "Enter keywords for news filtering (comma-separated)",
        value=default_keywords
    )
    
    fetch_button = st.button("Analyze Latest Headlines")
    
    if fetch_button:
        with st.spinner("Fetching and analyzing headlines..."):
            # Get exactly 20 relevant headlines
            news_data = scrape_news("NewsAPI", keywords, 20)
            
            if news_data and len(news_data) == 20:
                # Perform sentiment analysis
                results = analyze_sentiment(news_data)
                results_df = pd.DataFrame(results)
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["Headlines", "Sentiment Analysis", "Data Export"])
                
                with tab1:
                    st.markdown("### Latest Business Tech Headlines")
                    for idx, row in results_df.iterrows():
                        with st.expander(f"{row['title']} ({row['sentiment']})"):
                            st.write(f"Source: {row['source']}")
                            st.write(f"Country: {row['country']}")
                            st.write(f"Sentiment Score: {row['sentiment_score']:.2f}")
                            st.write(f"URL: {row['url']}")
                
                with tab2:
                    st.markdown("### Sentiment Distribution")
                    fig = create_sentiment_visualizations(results_df)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add sentiment statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Positive Headlines", 
                                len(results_df[results_df['sentiment'] == 'Positive']))
                    with col2:
                        st.metric("Neutral Headlines", 
                                len(results_df[results_df['sentiment'] == 'Neutral']))
                    with col3:
                        st.metric("Negative Headlines", 
                                len(results_df[results_df['sentiment'] == 'Negative']))
                
                with tab3:
                    st.markdown("### Export Data")
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        "Download Results CSV",
                        csv,
                        "news_sentiment_analysis.csv",
                        "text/csv"
                    )
            else:
                st.error("Could not fetch enough relevant headlines. Please try again.")

# About Page
elif page == "About":
    st.markdown("<div class='sub-header'>About This Project</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='highlight'>
    <h3>Assignment Details</h3>
    <p>This dashboard was created as part of the GUIDANCE – BIU TEAM ASSIGNMENT for Guidance Tamil Nadu.</p>
    
    <h4>Part 2: Web Scraping & Sentiment Analysis</h4>
    <p>The assignment required:</p>
    <ul>
        <li>Web scraping from publicly accessible news sources</li>
        <li>Collection of business headlines related to electronics, semiconductors, or manufacturing</li>
        <li>Extraction of title, URL, timestamp, and country mentioned</li>
        <li>Sentiment analysis using libraries like TextBlob or VADER</li>
        <li>Visualization of sentiment distribution</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Technologies Used</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Web Development**
        - Streamlit
        - Python
        - HTML/CSS
        """)
    
    with col2:
        st.markdown("""
        **Data Analysis**
        - Pandas
        - NumPy
        - NLTK
        """)
    
    with col3:
        st.markdown("""
        **Visualization**
        - Plotly
        - Matplotlib
        - WordCloud
        """)
# Add footer
st.markdown("""
<div class='footer'>
    <p>Submitted to: Guidance Tamil Nadu - BIU Team</p>
    <p>Assignment Part 2: Web Scraping & Sentiment Analysis</p>
    <p>© 2023 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)

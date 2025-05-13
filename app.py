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
    st.markdown("<div class='sub-header'>Real-Time News Sentiment Analysis</div>", unsafe_allow_html=True)
    
    # Auto-refresh settings
    refresh_interval = st.selectbox(
        "Auto-refresh interval",
        ["Off", "30 seconds", "1 minute", "5 minutes", "15 minutes"],
        help="Select how often to automatically fetch new headlines"
    )
    
    # Simplified news source selection - focusing on NewsAPI
    news_source = st.selectbox(
        "Select News Source",
        ["NewsAPI", "Manual Input"]
    )
    
    # Keywords for filtering news
    keywords = st.text_input(
        "Enter keywords for news filtering (comma-separated)",
        value="electronics, semiconductors, manufacturing"
    )
    
    # Number of articles to fetch
    num_articles = st.slider(
        "Number of latest articles to analyze",
        min_value=5,
        max_value=100,
        value=20
    )
    
    # Create a progress bar placeholder
    progress_bar = st.empty()
    
    # Add API status indicator
    st.sidebar.markdown("### API Status")
    try:
        response = requests.get(
            NEWS_API_ENDPOINTS['everything'],
            headers={'Authorization': f'Bearer {NEWS_API_KEY}'},
            params={'q': 'test', 'pageSize': 1}
        )
        if response.status_code == 200:
            st.sidebar.success("NewsAPI: Connected")
        else:
            st.sidebar.error(f"NewsAPI Error: {response.status_code}")
    except Exception as e:
        st.sidebar.error(f"NewsAPI Connection Error: {str(e)}")
    
    # Button to fetch and analyze news
    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_button = st.button("Fetch Latest News", key="fetch_analyze_button")
    with col2:
        if refresh_interval != "Off":
            st.info(f"Auto-refreshing every {refresh_interval}")
    
    if fetch_button or refresh_interval != "Off":
        # Initialize progress bar
        progress_bar = st.progress(0)
        
        with st.spinner("Fetching latest news and analyzing sentiment..."):
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
                    lines = manual_news.strip().split('\n')
                    
                    for i, line in enumerate(lines):
                        # Update progress
                        progress_bar.progress((i + 1) / len(lines))
                        
                        parts = [part.strip() for part in line.split(',')]
                        title = parts[0]
                        url = parts[1] if len(parts) > 1 else "N/A"
                        timestamp = parts[2] if len(parts) > 2 else "N/A"
                        country = parts[3] if len(parts) > 3 else "N/A"
                        
                        news_data.append({
                            'title': title,
                            'url': url,
                            'timestamp': timestamp,
                            'country': country,
                            'source': 'Manual Input'
                        })
                    
                    # Analyze sentiment
                    sentiment_results = analyze_sentiment(news_data)
                    
                    # Complete progress
                    progress_bar.progress(100)
                    
                    # Display results in tabs
                    tab1, tab2, tab3 = st.tabs(["Data Table", "Sentiment Distribution", "Source Analysis"])
                    
                    with tab1:
                        # Display results dataframe
                        st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                        results_df = pd.DataFrame(sentiment_results)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Add download button
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="news_sentiment_analysis.csv",
                            mime="text/csv"
                        )
                    
                    with tab2:
                        st.markdown("<div class='section-header'>Sentiment Analysis</div>", unsafe_allow_html=True)
                        # Create and display sentiment visualization
                        fig = create_sentiment_visualizations(results_df)
                        if fig is not None:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("Could not create sentiment visualization.")
                            
                    with tab3:
                        st.markdown("<div class='section-header'>Source Distribution</div>", unsafe_allow_html=True)
                        if 'source' in results_df.columns:
                            source_fig = px.pie(
                                results_df, 
                                names='source',
                                title='Distribution by News Source'
                            )
                            st.plotly_chart(source_fig, use_container_width=True)
            else:
                # Simulate progress for better UX
                for i in range(5):
                    progress_bar.progress(i * 20)
                    time.sleep(0.1)
                
                try:
                    # Scrape news from selected source
                    news_data = scrape_news(news_source, keywords.split(','), num_articles)
                    
                    # Complete progress
                    progress_bar.progress(100)
                    
                    if news_data:
                        # Analyze sentiment
                        sentiment_results = analyze_sentiment(news_data)
                        
                        # Display results in tabs
                        tab1, tab2, tab3 = st.tabs(["Data Table", "Sentiment Distribution", "Source Analysis"])
                        
                        with tab1:
                            # Display results dataframe
                            st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                            results_df = pd.DataFrame(sentiment_results)
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Add download button
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="Download Results as CSV",
                                data=csv,
                                file_name="news_sentiment_analysis.csv",
                                mime="text/csv"
                            )
                        
                        with tab2:
                            st.markdown("<div class='section-header'>Sentiment Analysis</div>", unsafe_allow_html=True)
                            # Create and display sentiment visualization
                            fig = create_sentiment_visualizations(results_df)
                            if fig is not None:
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.error("Could not create sentiment visualization.")
                                
                        with tab3:
                            st.markdown("<div class='section-header'>Source Distribution</div>", unsafe_allow_html=True)
                            if 'source' in results_df.columns:
                                source_fig = px.pie(
                                    results_df, 
                                    names='source',
                                    title='Distribution by News Source'
                                )
                                st.plotly_chart(source_fig, use_container_width=True)
                    else:
                        st.error("Failed to fetch news. Please try another source or check your internet connection.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Click the button above to fetch and analyze news headlines.")
        
        # Sample data for demonstration
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
            'timestamp': ['2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05'],
            'country': ['Global', 'China', 'Taiwan', 'USA', 'Global'],
            'sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative'],
            'sentiment_score': [0.65, -0.48, 0.72, 0.05, -0.52]
        }
        
        sample_df = pd.DataFrame(sample_sentiment)
        st.dataframe(sample_df, use_container_width=True)
        
        # Sample visualization
        fig = create_sentiment_visualizations(sample_df)
        st.plotly_chart(fig, use_container_width=True)

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

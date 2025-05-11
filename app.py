import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, create_sentiment_visualizations, create_timeline_visualization

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
        ["Google News", "NewsAPI", "Reuters", "Bloomberg", "Manual Input"]
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
    
    # Create a progress bar placeholder
    progress_bar = st.empty()
    
    # Button to fetch and analyze news
    fetch_button = st.button("Fetch and Analyze News", key="fetch_analyze_button")
    
    if fetch_button:
        # Initialize progress bar
        progress_bar = st.progress(0)
        
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
                    tab1, tab2, tab3 = st.tabs(["Data Table", "Sentiment Distribution", "Timeline"])
                    
                    with tab1:
                        # Display results
                        st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                        
                        # Create a DataFrame for display
                        results_df = pd.DataFrame(sentiment_results)
                        
                        # Display the dataframe
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
                        # Visualize sentiment distribution
                        st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                        
                        # Create visualization
                        fig = create_sentiment_visualizations(results_df)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with tab3:
                        st.markdown("<div class='section-header'>Sentiment Timeline</div>", unsafe_allow_html=True)
                        timeline_fig = create_timeline_visualization(results_df)
                        if timeline_fig:
                            st.plotly_chart(timeline_fig, use_container_width=True)
                        else:
                            st.warning("Timeline could not be generated. Make sure your news data includes valid timestamps.")
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
                        tab1, tab2, tab3 = st.tabs(["Data Table", "Sentiment Distribution", "Timeline"])
                        
                        with tab1:
                            # Display results
                            st.markdown("<div class='section-header'>News Headlines with Sentiment</div>", unsafe_allow_html=True)
                            
                            # Create a DataFrame for display
                            results_df = pd.DataFrame(sentiment_results)
                            
                            # Display the dataframe
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
                            # Visualize sentiment distribution
                            st.markdown("<div class='section-header'>Sentiment Distribution</div>", unsafe_allow_html=True)
                            
                            # Create visualization
                            fig = create_sentiment_visualizations(results_df)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Source distribution
                            if 'source' in results_df.columns:
                                source_fig = px.pie(
                                    results_df,
                                    names='source',
                                    title='News Source Distribution'
                                )
                                st.plotly_chart(source_fig, use_container_width=True)
                        
                        with tab3:
                            st.markdown("<div class='section-header'>Sentiment Timeline</div>", unsafe_allow_html=True)
                            timeline_fig = create_timeline_visualization(results_df)
                            if timeline_fig:
                                st.plotly_chart(timeline_fig, use_container_width=True)
                            else:
                                st.warning("Timeline could not be generated. Make sure your news data includes valid timestamps.")
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
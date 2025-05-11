"""
Tamil Nadu News Sentiment Analysis (Ultra Light Version)
This script scrapes news about Tamil Nadu's electronics, semiconductors, and manufacturing sectors,
performs sentiment analysis, and visualizes the results.
"""

import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
import re

# Set page configuration
st.set_page_config(
    page_title="Tamil Nadu Industry News Sentiment",
    page_icon="📰"
)

# Add title and description
st.title("📰 Tamil Nadu Industry News Sentiment Analysis")
st.markdown("""
This app scrapes the latest news about Tamil Nadu's electronics, semiconductors, and manufacturing sectors,
performs sentiment analysis on headlines, and visualizes the sentiment distribution.
""")

# Very simple sentiment analysis function (no NLTK dependency)
def get_sentiment(text):
    # Define positive and negative word lists
    positive_words = ['good', 'great', 'excellent', 'positive', 'growth', 'increase', 'success', 
                     'improve', 'boost', 'up', 'investment', 'opportunity', 'benefit', 'support', 
                     'win', 'lead', 'best', 'top', 'innovation', 'innovative', 'launch', 'expand']
    
    negative_words = ['bad', 'poor', 'negative', 'decline', 'decrease', 'fail', 'problem', 'issue', 
                     'crisis', 'down', 'loss', 'drop', 'fall', 'risk', 'concern', 'against', 'protest', 
                     'shortage', 'violation', 'warning', 'challenging', 'difficult', 'struggle']
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Count occurrences of positive and negative words
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    # Calculate simple sentiment score
    if positive_count > negative_count:
        return 'Positive', (positive_count - negative_count) / (positive_count + negative_count + 1)
    elif negative_count > positive_count:
        return 'Negative', -((negative_count - positive_count) / (positive_count + negative_count + 1))
    else:
        return 'Neutral', 0.0

# Function to extract location mentions
def extract_location(text):
    text_lower = text.lower()
    
    # Check for Tamil Nadu specifically
    if 'tamil nadu' in text_lower or 'tamilnadu' in text_lower:
        return 'Tamil Nadu'
    # Check for Chennai
    elif 'chennai' in text_lower:
        return 'Chennai'
    # Check for other major TN cities
    elif 'coimbatore' in text_lower:
        return 'Coimbatore'
    elif 'madurai' in text_lower:
        return 'Madurai'
    # If only India is mentioned
    elif 'india' in text_lower:
        return 'India'
    else:
        return 'Not specified'

# Function to scrape Google News
def scrape_google_news(keywords, max_results=20):
    news_list = []
    
    with st.spinner(f"Scraping Google News for {keywords}..."):
        try:
            # Combine keywords for search
            search_query = '+'.join(keywords)
            feed_url = f'https://news.google.com/rss/search?q={search_query}&hl=en-IN&gl=IN&ceid=IN:en'
            
            news_feed = feedparser.parse(feed_url)
            
            for entry in news_feed.entries[:max_results]:
                # Try to parse the date
                try:
                    pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                except:
                    pub_date = datetime.now()
                
                # Extract location mentions
                location = extract_location(entry.title)
                
                # Get sentiment
                sentiment, sentiment_score = get_sentiment(entry.title)
                
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'timestamp': pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'location': location,
                    'sentiment': sentiment,
                    'sentiment_score': sentiment_score
                })
                
        except Exception as e:
            st.error(f"Error scraping Google News: {e}")
    
    return news_list

# Define industry keywords
industry_options = [
    "electronics Tamil Nadu",
    "semiconductors Tamil Nadu",
    "manufacturing Tamil Nadu"
]

# Sidebar for controls
st.sidebar.title("Dashboard Controls")

selected_industries = st.sidebar.multiselect(
    "Select Industries to Track",
    options=["electronics", "semiconductors", "manufacturing"],
    default=["electronics", "semiconductors", "manufacturing"]
)

# Button to refresh data
if st.sidebar.button("Fetch News Data") or 'news_df' not in st.session_state:
    if not selected_industries:
        st.warning("Please select at least one industry to track.")
    else:
        # Convert selected industries to search terms
        search_terms = [f"{industry} Tamil Nadu" for industry in selected_industries]
        
        # Collect news from Google News
        all_news = []
        for term in search_terms:
            news = scrape_google_news([term], max_results=7)  # Get ~7 per category to reach ~20 total
            all_news.extend(news)
            
        # Remove duplicates and limit to 20 articles
        unique_news = []
        unique_titles = set()
        
        for news_item in all_news:
            if news_item['title'] not in unique_titles:
                unique_titles.add(news_item['title'])
                unique_news.append(news_item)
        
        # Create DataFrame
        if unique_news:
            news_df = pd.DataFrame(unique_news)
            if len(news_df) > 20:
                news_df = news_df.head(20)  # Limit to 20 articles as required
            st.session_state.news_df = news_df
        else:
            st.session_state.news_df = pd.DataFrame(columns=['title', 'url', 'timestamp', 'location', 'sentiment', 'sentiment_score'])
            st.warning("No news articles found. Try different search terms.")

# Display the dashboard if we have data
if 'news_df' in st.session_state and not st.session_state.news_df.empty:
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["📊 Sentiment Analysis", "📰 News Articles"])
    
    with tab1:
        st.header("News Sentiment Distribution")
        
        # Sentiment distribution chart
        sentiment_counts = st.session_state.news_df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        # Display as a simple table
        st.table(sentiment_counts)
        
        # Create a horizontal bar chart with native streamlit
        sentiment_order = {'Positive': 0, 'Neutral': 1, 'Negative': 2}
        sorted_counts = sentiment_counts.sort_values(by='Sentiment', key=lambda x: x.map(sentiment_order))
        
        colors = {
            'Positive': '#4CAF50',
            'Neutral': '#2196F3',
            'Negative': '#F44336'
        }
        
        # Create the chart with streamlit's native chart function
        st.bar_chart(
            sorted_counts.set_index('Sentiment'),
            use_container_width=True
        )

        # Summary statistics
        st.subheader("Summary Statistics")
        total_articles = len(st.session_state.news_df)
        positive_articles = sum(st.session_state.news_df['sentiment'] == 'Positive')
        neutral_articles = sum(st.session_state.news_df['sentiment'] == 'Neutral')
        negative_articles = sum(st.session_state.news_df['sentiment'] == 'Negative')
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Articles", total_articles)
        col2.metric("Positive", positive_articles, f"{positive_articles/total_articles:.1%}")
        col3.metric("Neutral", neutral_articles, f"{neutral_articles/total_articles:.1%}")
        col4.metric("Negative", negative_articles, f"{negative_articles/total_articles:.1%}")
        
        # Location mentions
        st.subheader("Locations Mentioned")
        
        # Count location occurrences
        location_counts = st.session_state.news_df['location'].value_counts().reset_index()
        location_counts.columns = ['Location', 'Count']
        
        if not location_counts.empty:
            st.table(location_counts)
        else:
            st.info("No specific locations mentioned in the news headlines.")
    
    with tab2:
        st.header("News Articles")
        
        # Add sentiment filters
        sentiment_filter = st.multiselect(
            "Filter by Sentiment",
            options=['Positive', 'Neutral', 'Negative'],
            default=['Positive', 'Neutral', 'Negative']
        )
        
        # Filter by sentiment
        filtered_df = st.session_state.news_df[st.session_state.news_df['sentiment'].isin(sentiment_filter)]
        
        # Sort options
        sort_options = st.radio(
            "Sort by",
            options=["Newest First", "Most Positive", "Most Negative"],
            horizontal=True
        )
        
        if sort_options == "Newest First":
            filtered_df = filtered_df.sort_values('timestamp', ascending=False)
        elif sort_options == "Most Positive":
            filtered_df = filtered_df.sort_values('sentiment_score', ascending=False)
        elif sort_options == "Most Negative":
            filtered_df = filtered_df.sort_values('sentiment_score', ascending=True)
        
        # Display news articles in a simple format
        for _, row in filtered_df.iterrows():
            st.markdown(f"""
            **{row['title']}**  
            *Location:* {row['location']} | *Published:* {row['timestamp']}  
            *Sentiment:* {row['sentiment']} ({row['sentiment_score']:.2f})  
            [Read Full Article]({row['url']})
            """)
            st.markdown("---")

else:
    # Display instructions if no data is present
    st.info("👈 Please select industries from the sidebar and click 'Fetch News Data' to get started!")
    
    st.markdown("""
    ## About This Dashboard
    
    This dashboard helps you track and analyze news related to Tamil Nadu's industrial sectors with a focus on sentiment analysis.
    
    ### Features:
    - Scrapes latest news from Google News RSS feed
    - Analyzes sentiment of headlines (Positive, Neutral, Negative)
    - Identifies locations mentioned in the news
    - Visualizes sentiment distribution
    
    ### Industries Covered:
    - Electronics
    - Semiconductors
    - Manufacturing
    
    Select your industries of interest from the sidebar and click "Fetch News Data" to begin!
    """)

# Footer
st.markdown("---")
st.markdown("📰 Tamil Nadu Industry News Sentiment Analysis | Created with Streamlit")

"""
Tamil Nadu News Sentiment Analysis
This script scrapes news about Tamil Nadu's electronics, semiconductors, and manufacturing sectors,
performs sentiment analysis, and visualizes the results.
"""

import streamlit as st
import pandas as pd
import feedparser
import matplotlib.pyplot as plt
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Set page configuration
st.set_page_config(
    page_title="Tamil Nadu Industry News Sentiment",
    page_icon="📰",
    layout="wide"
)

# Add title and description
st.title("📰 Tamil Nadu Industry News Sentiment Analysis")
st.markdown("""
This app scrapes the latest news about Tamil Nadu's electronics, semiconductors, and manufacturing sectors,
performs sentiment analysis on headlines, and visualizes the sentiment distribution.
""")

# Download VADER lexicon if not already downloaded
@st.cache_resource
def download_nltk_resources():
    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    return True

# Initialize sentiment analyzer
if download_nltk_resources():
    sid = SentimentIntensityAnalyzer()
else:
    st.error("Could not initialize sentiment analysis. Please check your internet connection.")
    st.stop()

# Function to determine sentiment category
def get_sentiment(text):
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        return 'Positive', compound_score
    elif compound_score <= -0.05:
        return 'Negative', compound_score
    else:
        return 'Neutral', compound_score

# Function to extract country mentions (with special focus on Tamil Nadu districts)
def extract_location(text):
    # Tamil Nadu districts
    tn_districts = [
        'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli',
        'Tiruppur', 'Vellore', 'Erode', 'Thoothukkudi', 'Dindigul', 'Thanjavur'
    ]
    
    # Check for Tamil Nadu districts
    found_locations = []
    text_lower = text.lower()
    
    # Check for Tamil Nadu specifically
    if 'tamil nadu' in text_lower or 'tamilnadu' in text_lower:
        found_locations.append('Tamil Nadu')
    
    # Check for districts
    for district in tn_districts:
        if district.lower() in text_lower:
            found_locations.append(district)
    
    # If no specific district but India is mentioned
    if not found_locations and ('india' in text_lower):
        found_locations.append('India')
    
    return ', '.join(found_locations) if found_locations else 'Not specified'

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

# Convert selected industries to search terms
search_terms = [f"{industry} Tamil Nadu" for industry in selected_industries]

# Button to refresh data
if st.sidebar.button("Fetch News Data") or 'news_df' not in st.session_state:
    if not selected_industries:
        st.warning("Please select at least one industry to track.")
    else:
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
        
        # Sort sentiment categories in a logical order
        sentiment_order = ['Positive', 'Neutral', 'Negative']
        sentiment_counts['Sentiment'] = pd.Categorical(
            sentiment_counts['Sentiment'], 
            categories=sentiment_order, 
            ordered=True
        )
        sentiment_counts = sentiment_counts.sort_values('Sentiment')
        
        # Define colors for sentiments
        colors = {
            'Positive': '#4CAF50',
            'Neutral': '#2196F3',
            'Negative': '#F44336'
        }
        
        # Create the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(
            sentiment_counts['Sentiment'],
            sentiment_counts['Count'],
            color=[colors[s] for s in sentiment_counts['Sentiment']]
        )
        
        # Add data labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.1,
                f'{height:.0f}',
                ha='center',
                va='bottom'
            )
        
        ax.set_xlabel('Sentiment', fontsize=12)
        ax.set_ylabel('Number of Articles', fontsize=12)
        ax.set_title('Sentiment Distribution of Tamil Nadu Industry News', fontsize=14)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Show the plot
        st.pyplot(fig)

        # Summary statistics
        st.subheader("Summary Statistics")
        total_articles = len(st.session_state.news_df)
        positive_articles = sum(st.session_state.news_df['sentiment'] == 'Positive')
        neutral_articles = sum(st.session_state.news_df['sentiment'] == 'Neutral')
        negative_articles = sum(st.session_state.news_df['sentiment'] == 'Negative')
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Articles", total_articles)
        col2.metric("Positive Articles", positive_articles, f"{positive_articles/total_articles:.1%}")
        col3.metric("Neutral Articles", neutral_articles, f"{neutral_articles/total_articles:.1%}")
        col4.metric("Negative Articles", negative_articles, f"{negative_articles/total_articles:.1%}")
        
        # Location mentions
        st.subheader("Locations Mentioned")
        
        # Extract all locations mentioned
        all_locations = []
        for loc in st.session_state.news_df['location']:
            if loc != 'Not specified':
                all_locations.extend(loc.split(', '))
        
        # Count occurrences
        location_counts = pd.Series(all_locations).value_counts()
        
        if not location_counts.empty:
            # Create a horizontal bar chart for locations
            fig, ax = plt.subplots(figsize=(10, 6))
            location_counts.head(10).plot(kind='barh', ax=ax)
            ax.set_xlabel('Number of Mentions')
            ax.set_ylabel('Location')
            ax.set_title('Top Locations Mentioned in News')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
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
        
        # Display news articles in a nice format
        for _, row in filtered_df.iterrows():
            sentiment_color = {
                'Positive': '#4CAF50',
                'Neutral': '#2196F3',
                'Negative': '#F44336'
            }.get(row['sentiment'], '#000000')
            
            st.markdown(f"""
            <div style="padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid {sentiment_color}; background-color: #f5f5f5;">
                <h4 style="margin-top: 0;">{row['title']}</h4>
                <p><strong>Location:</strong> {row['location']} | <strong>Published:</strong> {row['timestamp']}</p>
                <p><strong>Sentiment:</strong> <span style="color: {sentiment_color};">{row['sentiment']}</span> ({row['sentiment_score']:.2f})</p>
                <a href="{row['url']}" target="_blank">Read Full Article</a>
            </div>
            """, unsafe_allow_html=True)

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

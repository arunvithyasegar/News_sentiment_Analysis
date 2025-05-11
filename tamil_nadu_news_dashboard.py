"""
Tamil Nadu News Sentiment Analysis Dashboard
This Streamlit app scrapes news about Tamil Nadu from various sources,
performs sentiment analysis, and visualizes the results.
"""

# Import necessary libraries
import streamlit as st
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
import feedparser
import altair as alt
from PIL import Image
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Tamil Nadu News Sentiment Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Tamil Nadu News Sentiment Analysis\nCreated by Arun V"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        flex: 1;
        min-width: 120px;
        text-align: center;
    }
    .positive-text { color: #10B981; }
    .neutral-text { color: #6B7280; }
    .negative-text { color: #EF4444; }
    .news-item {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid;
    }
    .news-item.positive { border-left-color: #10B981; background-color: #ECFDF5; }
    .news-item.neutral { border-left-color: #6B7280; background-color: #F9FAFB; }
    .news-item.negative { border-left-color: #EF4444; background-color: #FEF2F2; }
    .source-tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        background-color: #E5E7EB;
        margin-right: 5px;
    }
    .location-tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        background-color: #DBEAFE;
        margin-right: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F3F4F6;
        border-bottom: 2px solid #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>📰 Tamil Nadu News Sentiment Analysis Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""
This dashboard scrapes the latest news about Tamil Nadu from various sources, 
analyzes the sentiment of headlines, and visualizes the results.
""")

# Create sidebar
st.sidebar.image("https://media.licdn.com/dms/image/v2/D5603AQER_Q4BRk3EOA/profile-displayphoto-shrink_200_200/B56ZYla9dOHEAY-/0/1744384547325?e=1752710400&v=beta&t=xhakBODVDf_3tgyYKPTce-GLdWDtZoU5XcThT_rGzbY", width=100)
st.sidebar.title("Dashboard Controls")

# Try to import NLTK and VADER with proper error handling
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
    # Download VADER lexicon if not already downloaded
    @st.cache_resource
    def download_nltk_resources():
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            try:
                nltk.download('vader_lexicon', quiet=True)
            except Exception as e:
                st.error(f"Failed to download VADER lexicon: {e}")
                return False
        return True
    
    # Initialize NLTK and VADER
    if not download_nltk_resources():
        st.error("Could not initialize sentiment analysis. Please check your internet connection.")
        st.stop()
    
    sid = SentimentIntensityAnalyzer()
    
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
    
except ImportError:
    st.error("NLTK is not installed. Using a simplified sentiment analysis approach.")
    
    # Fallback simple sentiment analysis function
    def get_sentiment(text):
        # Very simple sentiment analysis based on keywords
        positive_words = ['good', 'great', 'excellent', 'positive', 'growth', 'increase', 'success', 'improve']
        negative_words = ['bad', 'poor', 'negative', 'decline', 'decrease', 'fail', 'problem', 'issue', 'crisis']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            score = 0.5  # Simple positive score
            return 'Positive', score
        elif negative_count > positive_count:
            score = -0.5  # Simple negative score
            return 'Negative', score
        else:
            return 'Neutral', 0.0

# Function to extract country mentions (with special focus on Tamil Nadu districts)
def extract_location(text):
    # Tamil Nadu districts
    tn_districts = [
        'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli',
        'Tiruppur', 'Vellore', 'Erode', 'Thoothukkudi', 'Dindigul', 'Thanjavur',
        'Ranipet', 'Sivakasi', 'Karur', 'Udhagamandalam', 'Hosur', 'Nagercoil',
        'Kanchipuram', 'Kumarapalayam', 'Karaikkudi', 'Neyveli', 'Cuddalore',
        'Kanyakumari', 'Nilgiris', 'Theni', 'Krishnagiri', 'Villupuram', 'Namakkal'
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
    
    # If no specific district but Tamil Nadu is mentioned
    if not found_locations and ('india' in text_lower):
        found_locations.append('India')
    
    return ', '.join(found_locations) if found_locations else 'Not specified'

# Function to scrape Google News
def scrape_google_news(keywords, max_results=10):
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
                    pub_date = datetime.now() - timedelta(days=1)  # Default to yesterday
                
                # Extract location mentions
                location = extract_location(entry.title)
                
                # Get sentiment
                sentiment, sentiment_score = get_sentiment(entry.title)
                
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'timestamp': pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'Google News',
                    'location': location,
                    'sentiment': sentiment,
                    'sentiment_score': sentiment_score
                })
                
        except Exception as e:
            st.error(f"Error scraping Google News: {e}")
    
    return news_list

# Function to make safe HTTP requests
def safe_request(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        st.error(f"Error making request: {e}")
        return None

# Function to get news from NewsAPI
def get_news_from_newsapi(api_key, keywords, max_results=10):
    news_list = []
    
    with st.spinner("Fetching news from NewsAPI..."):
        try:
            # Prepare query with Tamil Nadu focus
            query_terms = " OR ".join(keywords)
            url = f'https://newsdata.io/api/1/news?apikey={api_key}&q=({query_terms}) AND (Tamil Nadu OR Chennai OR Coimbatore OR Madurai)&language=en'
            
            response = safe_request(url)
            if response is None:
                return []
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('results', [])
                
                for article in articles[:max_results]:
                    if article.get('title') and article.get('link'):
                        location = extract_location(article['title'])
                        
                        # Get sentiment
                        sentiment, sentiment_score = get_sentiment(article['title'])
                        
                        news_list.append({
                            'title': article['title'],
                            'url': article['link'],
                            'timestamp': article.get('pubDate', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            'source': article.get('source_id', 'NewsAPI'),
                            'location': location,
                            'sentiment': sentiment,
                            'sentiment_score': sentiment_score
                        })
            else:
                st.warning(f"NewsAPI returned status code {response.status_code}")
                
        except Exception as e:
            st.error(f"Error fetching from NewsAPI: {e}")
    
    return news_list

# Main function to collect and process news
def collect_and_analyze_news(api_key, search_areas):
    all_news = []
    
    # Tamil Nadu + search areas
    search_keywords = [area + " Tamil Nadu" for area in search_areas]
    
    # Get news from Google News
    google_results = scrape_google_news(search_keywords, max_results=15)
    all_news.extend(google_results)
    
    # Get news from NewsAPI if API key is provided
    if api_key:
        newsapi_results = get_news_from_newsapi(api_key, search_areas, max_results=15)
        all_news.extend(newsapi_results)
    
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
        return news_df
    else:
        return pd.DataFrame(columns=['title', 'url', 'timestamp', 'source', 'location', 'sentiment', 'sentiment_score'])

# Add this after the news collection functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_news(api_key, search_areas):
    try:
        df = collect_and_analyze_news(api_key, search_areas)
        if df is not None and not df.empty:
            return df
        return pd.DataFrame(columns=['title', 'url', 'timestamp', 'source', 'location', 'sentiment', 'sentiment_score'])
    except Exception as e:
        st.error(f"Error collecting news: {e}")
        return pd.DataFrame(columns=['title', 'url', 'timestamp', 'source', 'location', 'sentiment', 'sentiment_score'])

# NewsAPI key input (with a default value for demo)
api_key = st.sidebar.text_input("Enter NewsAPI Key", value="pub_86076086703c94c2637e240672a4a90a30ad9")

# Industry selection
industry_options = [
    "electronics",
    "semiconductors",
    "manufacturing",
    "technology",
    "automotive",
    "textiles",
    "IT",
    "renewable energy"
]

selected_industries = st.sidebar.multiselect(
    "Select Industries to Track",
    options=industry_options,
    default=["electronics", "semiconductors", "manufacturing"]
)

# Button to refresh data
if st.sidebar.button("Refresh Data"):
    if not selected_industries:
        st.warning("Please select at least one industry to track.")
    else:
        with st.spinner("Collecting and analyzing news..."):
            try:
                st.session_state.news_df = get_cached_news(api_key, selected_industries)
                if st.session_state.news_df.empty:
                    st.warning("No news articles found. Try different search terms or check your API key.")
            except Exception as e:
                st.error(f"Error refreshing data: {e}")

# Initialize session state for news_df if it doesn't exist
if 'news_df' not in st.session_state:
    st.session_state.news_df = pd.DataFrame(columns=['title', 'url', 'timestamp', 'source', 'location', 'sentiment', 'sentiment_score'])

# Display the dashboard if we have data
if not st.session_state.news_df.empty:
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "📊 Detailed Analysis", "📰 News Articles"])
    
    with tab1:
        st.header("News Sentiment Overview")
        
        # Create two columns for visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution chart
            sentiment_counts = st.session_state.news_df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            
            # Define colors for sentiments
            colors = {
                'Positive': '#4CAF50',
                'Neutral': '#2196F3',
                'Negative': '#F44336'
            }
            
            # Create bar chart
            fig = px.bar(
                sentiment_counts,
                x='Sentiment',
                y='Count',
                title='Sentiment Distribution',
                color='Sentiment',
                color_discrete_map=colors,
                text='Count'
            )
            
            fig.update_layout(
                xaxis_title='Sentiment',
                yaxis_title='Number of Articles',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Source distribution pie chart
            source_counts = st.session_state.news_df['source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Count']
            
            fig2 = px.pie(
                source_counts,
                names='Source',
                values='Count',
                title='News Sources',
                hole=0.4
            )
            
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Location mentions
        st.subheader("Location Mentions")
        
        # Extract all locations mentioned
        all_locations = []
        for loc in st.session_state.news_df['location']:
            if loc != 'Not specified':
                all_locations.extend(loc.split(', '))
        
        # Count occurrences
        location_counts = pd.Series(all_locations).value_counts().reset_index()
        location_counts.columns = ['Location', 'Mentions']
        
        if not location_counts.empty:
            # Create horizontal bar chart for locations
            fig3 = px.bar(
                location_counts.head(10),  # Top 10 locations
                y='Location',
                x='Mentions',
                title='Top Locations Mentioned',
                orientation='h',
                color='Mentions',
                color_continuous_scale=px.colors.sequential.Viridis
            )
            
            fig3.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No specific locations mentioned in the news headlines.")
    
    with tab2:
        st.header("Detailed Sentiment Analysis")
        
        # Sentiment over time
        st.session_state.news_df['date'] = pd.to_datetime(st.session_state.news_df['timestamp'])
        st.session_state.news_df = st.session_state.news_df.sort_values('date')
        
        # Create a line chart of sentiment scores over time
        fig4 = px.line(
            st.session_state.news_df,
            x='date',
            y='sentiment_score',
            title='Sentiment Trend Over Time',
            markers=True
        )
        
        fig4.update_layout(
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            yaxis=dict(range=[-1, 1]),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Add horizontal lines for sentiment boundaries
        fig4.add_shape(
            type="line",
            x0=st.session_state.news_df['date'].min(),
            y0=0.05,
            x1=st.session_state.news_df['date'].max(),
            y1=0.05,
            line=dict(color="green", width=1, dash="dash"),
        )
        
        fig4.add_shape(
            type="line",
            x0=st.session_state.news_df['date'].min(),
            y0=-0.05,
            x1=st.session_state.news_df['date'].max(),
            y1=-0.05,
            line=dict(color="red", width=1, dash="dash"),
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        
        # Industry-specific analysis
        st.subheader("Industry-Specific Analysis")
        
        industry_sentiments = {}
        for industry in selected_industries:
            # Filter headlines that mention this industry
            industry_news = st.session_state.news_df[st.session_state.news_df['title'].str.contains(industry, case=False)]
            
            if not industry_news.empty:
                positive = sum(industry_news['sentiment'] == 'Positive')
                neutral = sum(industry_news['sentiment'] == 'Neutral')
                negative = sum(industry_news['sentiment'] == 'Negative')
                avg_score = industry_news['sentiment_score'].mean()
                
                industry_sentiments[industry] = {
                    'positive': positive,
                    'neutral': neutral,
                    'negative': negative,
                    'total': len(industry_news),
                    'avg_score': avg_score
                }
        
        if industry_sentiments:
            # Convert to DataFrame for visualization
            industry_df = pd.DataFrame([
                {'Industry': ind, 'Avg. Sentiment': data['avg_score'], 'Articles': data['total']}
                for ind, data in industry_sentiments.items()
            ])
            
            # Create industry sentiment comparison
            fig5 = px.bar(
                industry_df,
                x='Industry',
                y='Avg. Sentiment',
                title='Average Sentiment by Industry',
                color='Avg. Sentiment',
                size='Articles',
                color_continuous_scale=px.colors.diverging.RdBu,
                color_continuous_midpoint=0
            )
            
            fig5.update_layout(
                xaxis_title='Industry',
                yaxis_title='Average Sentiment Score',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig5, use_container_width=True)
            
    with tab3:
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
            filtered_df = filtered_df.sort_values('date', ascending=False)
        elif sort_options == "Most Positive":
            filtered_df = filtered_df.sort_values('sentiment_score', ascending=False)
        elif sort_options == "Most Negative":
            filtered_df = filtered_df.sort_values('sentiment_score', ascending=True)
        
        # Display news articles
        def display_news_item(row):
            sentiment_colors = {
                'Positive': '#ECFDF5',
                'Neutral': '#F9FAFB',
                'Negative': '#FEF2F2'
            }
            border_colors = {
                'Positive': '#10B981',
                'Neutral': '#6B7280',
                'Negative': '#EF4444'
            }
            
            bg_color = sentiment_colors.get(row['sentiment'], '#F9FAFB')
            border_color = border_colors.get(row['sentiment'], '#6B7280')
            
            st.markdown(f"""
            <div style="padding:15px; border-radius:5px; margin-bottom:10px; 
                        background-color:{bg_color}; border-left:5px solid {border_color};">
                <h4 style="margin-top:0;">{row['title']}</h4>
                <p>
                    <span class='source-tag'>{row['source']}</span>
                    <span class='location-tag'>{row['location']}</span>
                    <span>{row['timestamp']}</span>
                </p>
                <a href="{row['url']}" target="_blank">Read Full Article</a>
            </div>
            """, unsafe_allow_html=True)
        
        if not filtered_df.empty:
            for _, row in filtered_df.iterrows():
                display_news_item(row)
        else:
            st.info("No news articles found. Try adjusting your search terms or refreshing the data.")

# Add Tamil Nadu investment context at the bottom of sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Tamil Nadu Industry Context")
st.sidebar.info("""
Tamil Nadu is a major industrial hub in India with significant investments in:

- Electronics manufacturing
- Automobile production
- Textiles and garments
- Information Technology
- Renewable energy

The state has attracted major semiconductor and electronics companies for investments.
""")

# Add instructions for first-time visitors
if st.session_state.news_df.empty:
    st.info("👈 Please select industries from the sidebar and click 'Refresh Data' to get started!")
    
    # Show a Tamil Nadu map in the center
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/TN_India.png/800px-TN_India.png", caption="Tamil Nadu State Map")
    
    # Add introduction text
    st.markdown("""
    ## About This Dashboard
    
    This dashboard helps you track and analyze news related to Tamil Nadu's industrial sectors with a focus on sentiment analysis.
    
    ### Features:
    - Scrapes latest news from multiple sources
    - Analyzes sentiment of headlines (Positive, Neutral, Negative)
    - Identifies locations mentioned in the news
    - Tracks sentiment trends over time
    - Provides industry-specific sentiment analysis
    
    ### Industries Covered:
    - Electronics and Semiconductors
    - Manufacturing
    - Technology and IT
    - Automotive
    - Textiles
    - Renewable Energy
    
    Select your industries of interest from the sidebar and click "Refresh Data" to begin!
    """)

# Footer
st.markdown("---")
st.markdown("📰 Tamil Nadu News Sentiment Analysis Dashboard • Created with Streamlit")

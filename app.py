import streamlit as st
import pandas as pd
import plotly.express as px
from news_scraper import scrape_news
from sentiment_analysis import analyze_sentiment, create_sentiment_visualizations
import datetime

# Page config
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

# Title and description
st.title("News Sentiment Analysis")
st.markdown("Analyze sentiment of news headlines related to electronics and semiconductors")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    news_source = st.selectbox("Select News Source", ["Google News"])
    keywords = st.text_input(
        "Keywords (comma-separated)",
        value="electronics, semiconductors, manufacturing",
        help="Enter keywords to search for in news headlines"
    )
    num_articles = st.slider("Number of articles", 5, 30, 20)
    
# Main content
if st.button("Fetch and Analyze News"):
    with st.spinner("Fetching news..."):
        try:
            # Fetch news
            news_data = scrape_news(news_source, keywords.split(","), num_articles)
            
            if not news_data:
                st.error("No news articles found. Try different keywords.")
                st.stop()
            
            # Analyze sentiment
            sentiment_results = analyze_sentiment(news_data)
            
            # Create DataFrame
            df = pd.DataFrame(sentiment_results)
            
            # Display results
            st.subheader("News Headlines")
            st.dataframe(
                df[['title', 'sentiment', 'sentiment_score', 'source', 'country']],
                use_container_width=True
            )
            
            # Show visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_sentiment_visualizations(df),
                    use_container_width=True
                )
            
            with col2:
                # Source distribution
                fig = px.pie(
                    df,
                    names='source',
                    title='News Source Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Save results
            st.download_button(
                "Download Results",
                df.to_csv(index=False),
                "news_sentiment_analysis.csv",
                "text/csv"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Click the button above to fetch and analyze news headlines.")
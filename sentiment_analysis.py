import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px
import pandas as pd

# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(news_data):
    """Analyze sentiment of news headlines using VADER"""
    sid = SentimentIntensityAnalyzer()
    
    for article in news_data:
        scores = sid.polarity_scores(article['title'])
        article['sentiment_score'] = scores['compound']
        
        if scores['compound'] >= 0.05:
            article['sentiment'] = 'Positive'
        elif scores['compound'] <= -0.05:
            article['sentiment'] = 'Negative'
        else:
            article['sentiment'] = 'Neutral'
    
    return news_data

def create_sentiment_visualizations(df):
    """Create interactive visualizations for sentiment analysis"""
    # Sentiment distribution
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    color_map = {'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'}
    
    fig = px.bar(
        sentiment_counts,
        x='Sentiment',
        y='Count',
        title='Sentiment Distribution of News Headlines',
        color='Sentiment',
        color_discrete_map=color_map,
        text='Count'
    )
    
    fig.update_layout(
        xaxis_title='Sentiment Category',
        yaxis_title='Number of Headlines',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
import pandas as pd

def analyze_sentiment(news_data):
    """Analyze sentiment of news headlines using VADER"""
    analyzer = SentimentIntensityAnalyzer()
    
    analyzed_data = []
    for article in news_data:
        sentiment = analyzer.polarity_scores(article['title'])
        
        # Determine sentiment category
        if sentiment['compound'] >= 0.05:
            sentiment_category = 'Positive'
        elif sentiment['compound'] <= -0.05:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
            
        analyzed_data.append({
            'title': article['title'],
            'url': article['url'],
            'timestamp': article['timestamp'],
            'source': article.get('source', 'Unknown'),
            'country': article['country'],
            'sentiment': sentiment_category,
            'sentiment_score': sentiment['compound']
        })
    
    return analyzed_data

def create_sentiment_visualizations(df):
    """Create required sentiment visualizations"""
    # Convert sentiment distribution to count
    sentiment_counts = df['sentiment'].value_counts()
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=['Positive', 'Neutral', 'Negative'],
            y=[
                sentiment_counts.get('Positive', 0),
                sentiment_counts.get('Neutral', 0),
                sentiment_counts.get('Negative', 0)
            ],
            marker_color=['#2ecc71', '#95a5a6', '#e74c3c']
        )
    ])
    
    fig.update_layout(
        title='Sentiment Distribution Across Headlines',
        xaxis_title='Sentiment Category',
        yaxis_title='Number of Headlines',
        showlegend=False
    )
    
    return fig
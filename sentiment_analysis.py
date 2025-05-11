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
    try:
        # Ensure we have sentiment data
        if 'sentiment' not in df.columns:
            return None
            
        # Calculate sentiment counts
        sentiment_counts = df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        # Define consistent colors
        color_map = {'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'}
        
        # Create figure with both bar chart and pie chart
        fig = px.bar(
            sentiment_counts,
            x='Sentiment',
            y='Count',
            color='Sentiment',
            color_discrete_map=color_map,
            title='Sentiment Distribution'
        )
        
        # Update layout for better visibility
        fig.update_layout(
            showlegend=True,
            xaxis_title="Sentiment Category",
            yaxis_title="Number of Articles",
            plot_bgcolor='white',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5
        )
        
        # Add value labels on bars
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        return fig
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        return None

def create_timeline_visualization(results_df):
    """Create timeline visualization of sentiment scores"""
    if 'timestamp' in results_df.columns:
        try:
            time_df = results_df.copy()
            time_df['date'] = pd.to_datetime(time_df['timestamp'])
            time_df = time_df.sort_values('date')
            
            fig = px.scatter(
                time_df, 
                x='date', 
                y='sentiment_score',
                color='sentiment',
                size_max=10,
                hover_data=['title', 'source'],
                color_discrete_map={
                    'Positive': '#4CAF50',
                    'Neutral': '#2196F3',
                    'Negative': '#F44336'
                }
            )
            
            fig.update_layout(
                title='News Sentiment Timeline',
                xaxis_title='Publication Date',
                yaxis_title='Sentiment Score',
                hovermode='closest',
                height=400
            )
            
            return fig
        except Exception as e:
            print(f"Timeline creation error: {str(e)}")
            return None
    return None
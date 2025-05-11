import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_sentiment_category(score):
    """
    Convert sentiment score to category
    
    Parameters:
    score (float): Sentiment score from VADER
    
    Returns:
    str: Sentiment category (Positive, Neutral, Negative)
    """
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_sentiment(news_data):
    """
    Analyze sentiment of news headlines
    
    Parameters:
    news_data (list): List of dictionaries containing news data
    
    Returns:
    list: List of dictionaries with sentiment analysis added
    """
    # Initialize VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    
    # Add sentiment analysis to each news item
    for item in news_data:
        # Get sentiment scores
        sentiment_scores = sid.polarity_scores(item['title'])
        
        # Add sentiment score and category
        item['sentiment_score'] = sentiment_scores['compound']
        item['sentiment'] = get_sentiment_category(sentiment_scores['compound'])
    
    return news_data

def visualize_sentiment(sentiment_results):
    """
    Create visualization of sentiment distribution
    
    Parameters:
    sentiment_results (list): List of dictionaries with sentiment analysis
    
    Returns:
    matplotlib.figure.Figure: Figure object with visualization
    """
    # Convert to DataFrame
    df = pd.DataFrame(sentiment_results)
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts()
    
    # Define colors for sentiment categories
    colors = {'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#F44336'}
    bar_colors = [colors[sentiment] for sentiment in sentiment_counts.index]
    
    # Create bar chart
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=bar_colors, ax=ax)
    
    # Add labels and title
    ax.set_title('Sentiment Distribution of News Headlines', fontsize=16)
    ax.set_xlabel('Sentiment Category', fontsize=12)
    ax.set_ylabel('Number of Headlines', fontsize=12)
    
    # Add count labels on top of bars
    for i, count in enumerate(sentiment_counts.values):
        ax.text(i, count + 0.5, str(count), ha='center', fontsize=12)
    
    # Improve aesthetics
    plt.tight_layout()
    
    return fig
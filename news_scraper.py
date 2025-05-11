import requests
import pandas as pd
from datetime import datetime

def scrape_news(source, keywords, num_articles):
    """
    Scrape news articles from various sources based on keywords
    
    Parameters:
    source (str): The news source to scrape from (NewsAPI, Reuters, Bloomberg)
    keywords (list): List of keywords to filter news
    num_articles (int): Number of articles to retrieve
    
    Returns:
    list: List of dictionaries containing news data
    """
    news_data = []
    
    try:
        if source == "NewsAPI":
            # Using NewsData.io API (similar to what you used in your notebooks)
            api_key = "pub_86076086703c94c2637e240672a4a90a30ad9"  # Replace with your actual API key if different
            
            for keyword in keywords:
                url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={keyword}&language=en&category=business,technology"
                
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('results', [])
                    
                    for article in articles:
                        if len(news_data) >= num_articles:
                            break
                            
                        if article.get('title') and article.get('link'):
                            news_data.append({
                                'title': article['title'],
                                'url': article['link'],
                                'timestamp': article.get('pubDate', 'Unknown'),
                                'source': article.get('source_id', 'NewsAPI'),
                                'country': article.get('country', ['Unknown'])[0] if isinstance(article.get('country'), list) else 'Unknown'
                            })
        
        elif source == "Reuters" or source == "Bloomberg":
            # For demonstration purposes, return sample data
            # In a real implementation, you would use web scraping or their APIs
            sample_sources = {
                "Reuters": "Reuters News",
                "Bloomberg": "Bloomberg News"
            }
            
            for i in range(min(num_articles, 10)):
                news_data.append({
                    'title': f"Sample {keywords[i % len(keywords)]} news article {i+1}",
                    'url': f"https://example.com/article{i+1}",
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'source': sample_sources.get(source, source),
                    'country': "Global"
                })
    
    except Exception as e:
        print(f"Error scraping news: {e}")
        return []
    
    return news_data[:num_articles]
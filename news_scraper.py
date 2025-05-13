import feedparser
import requests
from datetime import datetime, timedelta
import time
import pycountry
import re
from urllib.parse import quote_plus
from config import NEWS_API_KEY, NEWS_API_ENDPOINTS

def extract_countries(text):
    """Extract country mentions from text"""
    country_list = [country.name for country in pycountry.countries]
    found_countries = []
    for country in country_list:
        if re.search(r'\b' + re.escape(country) + r'\b', text, re.IGNORECASE):
            found_countries.append(country)
    return ', '.join(found_countries) if found_countries else 'Not specified'

def scrape_google_news(keywords, num_articles=5):
    """Scrape news from Google News RSS feed with improved URL handling"""
    articles = []
    
    try:
        # Clean and prepare keywords
        cleaned_keywords = [keyword.strip() for keyword in keywords]
        query = quote_plus(" ".join(cleaned_keywords))
        
        feed_url = f'https://news.google.com/rss/search?q={query}+business&hl=en-US&gl=US&ceid=US:en'
        news_feed = feedparser.parse(feed_url)
        
        if news_feed.entries:
            for entry in news_feed.entries[:num_articles]:
                try:
                    articles.append({
                        'title': entry.title,
                        'url': entry.link,
                        'timestamp': datetime.strptime(
                            entry.published, 
                            '%a, %d %b %Y %H:%M:%S %Z'
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        'source': 'Google News',
                        'country': extract_countries(entry.title)
                    })
                    time.sleep(0.1)  # Polite delay between requests
                except Exception as e:
                    print(f"Error processing entry: {str(e)}")
                    continue
                    
    except Exception as e:
        print(f"Error fetching Google News: {str(e)}")
        return None
    
    return articles

def fetch_from_newsapi(keywords, num_articles):
    headers = {'Authorization': f'Bearer {NEWS_API_KEY}'}
    
    # Join keywords with OR for the query
    query = ' OR '.join(k.strip() for k in keywords)
    
    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'q': query,
        'pageSize': min(num_articles, 100),  # NewsAPI limit is 100
        'language': 'en',
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'sortBy': 'publishedAt'
    }
    
    try:
        response = requests.get(
            NEWS_API_ENDPOINTS['everything'],
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                {
                    'title': article['title'],
                    'url': article['url'],
                    'timestamp': article['publishedAt'],
                    'source': article['source']['name'],
                    'country': article.get('country', 'N/A')
                }
                for article in articles
            ]
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def scrape_news(source, keywords, num_articles=20):
    """Main function to scrape news from selected source with error handling"""
    try:
        if source == "Google News":
            return scrape_google_news(keywords, num_articles)
        elif source == "NewsAPI":
            return fetch_from_newsapi(keywords, num_articles)
        else:
            # Fallback to Google News if selected source is not implemented
            print(f"Source {source} not implemented, falling back to Google News")
            return scrape_google_news(keywords, num_articles)
    except Exception as e:
        print(f"Error in news scraping: {str(e)}")
        return None
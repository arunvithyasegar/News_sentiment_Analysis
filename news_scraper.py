import feedparser
import requests
from datetime import datetime, timedelta
import time
import pycountry
import re
from urllib.parse import quote_plus
try:
    from config import (NEWS_API_KEY, NEWS_API_ENDPOINTS, 
                       GNEWS_API_KEY, GNEWS_API_ENDPOINTS)
except ImportError:
    print("Config file not found. Using default settings.")
    NEWS_API_KEY = "7afdf16c-ecc6-4589-a79e-4f5224c6aa08"
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    NEWS_API_ENDPOINTS = {
        "everything": f"{NEWS_API_BASE_URL}/everything",
        "top-headlines": f"{NEWS_API_BASE_URL}/top-headlines"
    }
    GNEWS_API_KEY = "your_gnews_api_key"
    GNEWS_API_BASE_URL = "https://gnews.io/api/v4"
    GNEWS_API_ENDPOINTS = {
        "search": f"{GNEWS_API_BASE_URL}/search"
    }

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
    if not NEWS_API_KEY:
        raise ValueError("NewsAPI key is not configured")
    
    headers = {'X-Api-Key': NEWS_API_KEY}  # Changed from Bearer to X-Api-Key
    
    # Join keywords with OR for the query
    query = ' OR '.join(k.strip() for k in keywords)
    
    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'q': query,
        'pageSize': min(num_articles, 100),
        'language': 'en',
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'sortBy': 'publishedAt'
    }
    
    try:
        endpoint = NEWS_API_ENDPOINTS.get('everything')
        if not endpoint:
            raise ValueError("NewsAPI endpoint not configured")
            
        response = requests.get(
            endpoint,
            headers=headers,
            params=params
        )
        
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        
        if data.get('status') != 'ok':
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
            
        articles = data.get('articles', [])
        return [
            {
                'title': article['title'],
                'url': article['url'],
                'timestamp': article['publishedAt'],
                'source': article['source']['name'],
                'country': extract_countries(article['title'])
            }
            for article in articles
        ]
            
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {str(e)}")
        return []
    except ValueError as e:
        print(f"API Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return []

def fetch_from_gnews(keywords, num_articles):
    """Fetch news from GNews API"""
    if not GNEWS_API_KEY:
        raise ValueError("GNews API key is not configured")
    
    # Join keywords with AND for better results
    query = ' AND '.join(k.strip() for k in keywords)
    
    params = {
        'q': query,
        'token': GNEWS_API_KEY,
        'max': min(num_articles, 100),
        'lang': 'en',
        'sortby': 'publishedAt'
    }
    
    try:
        endpoint = GNEWS_API_ENDPOINTS.get('search')
        if not endpoint:
            raise ValueError("GNews API endpoint not configured")
            
        response = requests.get(
            endpoint,
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        return [
            {
                'title': article['title'],
                'url': article['url'],
                'timestamp': article['publishedAt'],
                'source': article['source']['name'],
                'country': extract_countries(article['title'])
            }
            for article in articles
        ]
            
    except requests.exceptions.RequestException as e:
        print(f"GNews API Network Error: {str(e)}")
        return []
    except Exception as e:
        print(f"GNews API Error: {str(e)}")
        return []

def filter_business_tech_news(articles, keywords):
    """Filter articles related to electronics, semiconductors, or manufacturing"""
    tech_keywords = [
        'electronics', 'semiconductor', 'manufacturing', 'chip', 'technology',
        'processor', 'hardware', 'circuit', 'production', 'factory'
    ]
    
    filtered_articles = []
    for article in articles:
        title = article['title'].lower()
        if any(keyword.lower() in title for keyword in tech_keywords):
            filtered_articles.append(article)
    
    return filtered_articles

def scrape_news(source, keywords, num_articles=20):
    """Main function to scrape exactly 20 relevant business tech headlines"""
    if not isinstance(keywords, list):
        keywords = [k.strip() for k in keywords.split(',')]
    
    # Request more articles initially to ensure we get enough after filtering
    fetch_count = min(100, num_articles * 3)
    
    try:
        results = []
        
        # Try multiple sources if needed to get enough articles
        for api_source in [fetch_from_newsapi, fetch_from_gnews, scrape_google_news]:
            if len(results) >= num_articles:
                break
                
            try:
                new_articles = api_source(keywords, fetch_count)
                if new_articles:
                    # Filter for relevant articles
                    filtered = filter_business_tech_news(new_articles, keywords)
                    results.extend(filtered)
            except Exception as e:
                print(f"Error with source {api_source.__name__}: {str(e)}")
        
        # Ensure we return exactly num_articles results
        return results[:num_articles] if results else []
            
    except Exception as e:
        print(f"Error in news scraping: {str(e)}")
        return []
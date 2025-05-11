import feedparser
import requests
from datetime import datetime
import time
import pycountry
import re
from urllib.parse import quote_plus

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

def scrape_news(source, keywords, num_articles=20):
    """Main function to scrape news from selected source with error handling"""
    try:
        if source == "Google News":
            return scrape_google_news(keywords, num_articles)
        else:
            # Fallback to Google News if selected source is not implemented
            print(f"Source {source} not implemented, falling back to Google News")
            return scrape_google_news(keywords, num_articles)
    except Exception as e:
        print(f"Error in news scraping: {str(e)}")
        return None
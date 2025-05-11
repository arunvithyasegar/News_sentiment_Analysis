import feedparser
import requests
from datetime import datetime
import time
import pycountry
import re

def extract_countries(text):
    """Extract country mentions from text"""
    country_list = [country.name for country in pycountry.countries]
    found_countries = []
    for country in country_list:
        if re.search(r'\b' + re.escape(country) + r'\b', text, re.IGNORECASE):
            found_countries.append(country)
    return ', '.join(found_countries) if found_countries else 'Not specified'

def scrape_google_news(keywords, num_articles=5):
    """Scrape news from Google News RSS feed"""
    articles = []
    
    for keyword in keywords:
        feed_url = f'https://news.google.com/rss/search?q={keyword}+business&hl=en-US&gl=US&ceid=US:en'
        news_feed = feedparser.parse(feed_url)
        
        for entry in news_feed.entries[:num_articles]:
            articles.append({
                'title': entry.title,
                'url': entry.link,
                'timestamp': datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Google News',
                'country': extract_countries(entry.title)
            })
            time.sleep(0.1)
            
    return articles

def scrape_news(source, keywords, num_articles=20):
    """Main function to scrape news from selected source"""
    if source == "Google News":
        return scrape_google_news(keywords, num_articles)
    else:
        # Add other news sources as needed
        return scrape_google_news(keywords, num_articles)
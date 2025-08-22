import requests
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

class NewsAPIClient:
    """Client for interacting with NewsAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a request to NewsAPI with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params['apiKey'] = self.api_key
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Exception("Invalid API key. Please check your NewsAPI key.")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait before making more requests.")
            else:
                raise Exception(f"API request failed with status {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise Exception("Request timeout. Please try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def search_articles(self, query: str, from_date: str = None, 
                       sort_by: str = 'publishedAt', language: str = 'en',
                       page_size: int = 20) -> List[Dict]:
        """Search for articles based on query"""
        
        # Check cache first
        cache_key = f"search_{query}_{from_date}_{sort_by}_{language}_{page_size}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        params = {
            'q': query,
            'sortBy': sort_by,
            'language': language,
            'pageSize': page_size
        }
        
        if from_date:
            params['from'] = from_date
        
        try:
            result = self._make_request('everything', params)
            articles = result.get('articles', [])
            
            # Cache the result
            self.cache[cache_key] = (articles, time.time())
            
            return articles
            
        except Exception as e:
            print(f"Error searching articles for '{query}': {str(e)}")
            return []
    
    def get_top_headlines(self, country: str = 'us', category: str = None,
                         page_size: int = 20) -> List[Dict]:
        """Get top headlines for a country/category"""
        
        cache_key = f"headlines_{country}_{category}_{page_size}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        params = {
            'country': country,
            'pageSize': page_size
        }
        
        if category:
            params['category'] = category
        
        try:
            result = self._make_request('top-headlines', params)
            articles = result.get('articles', [])
            
            # Cache the result
            self.cache[cache_key] = (articles, time.time())
            
            return articles
            
        except Exception as e:
            print(f"Error getting top headlines: {str(e)}")
            return []
    
    def get_sources(self, category: str = None, language: str = 'en',
                   country: str = 'us') -> List[Dict]:
        """Get available news sources"""
        
        cache_key = f"sources_{category}_{language}_{country}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        params = {
            'language': language,
            'country': country
        }
        
        if category:
            params['category'] = category
        
        try:
            result = self._make_request('sources', params)
            sources = result.get('sources', [])
            
            # Cache the result
            self.cache[cache_key] = (sources, time.time())
            
            return sources
            
        except Exception as e:
            print(f"Error getting sources: {str(e)}")
            return []
    
    def fetch_articles_by_interests(self, interests: List[str], 
                                  frequency: str = 'daily') -> List[Dict]:
        """Fetch articles based on user interests and frequency"""
        
        all_articles = []
        
        # Define keywords for each interest
        interest_keywords = {
            'Technology': ['artificial intelligence', 'cybersecurity', 'software', 'hardware', 'startups'],
            'Business': ['finance', 'economy', 'markets', 'entrepreneurship', 'corporate'],
            'Science': ['research', 'discoveries', 'health', 'environment', 'space'],
            'Politics': ['government', 'policy', 'elections', 'international relations'],
            'Sports': ['football', 'basketball', 'tennis', 'olympics', 'soccer'],
            'Entertainment': ['movies', 'music', 'celebrity', 'gaming', 'streaming']
        }
        
        # Calculate date range
        if frequency == 'daily':
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        else:  # weekly
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        for interest in interests:
            if interest in interest_keywords:
                for keyword in interest_keywords[interest][:2]:  # Limit keywords per interest
                    articles = self.search_articles(
                        query=keyword,
                        from_date=from_date,
                        page_size=5
                    )
                    
                    # Add category and keyword metadata
                    for article in articles:
                        article['category'] = interest
                        article['keyword'] = keyword
                    
                    all_articles.extend(articles)
                    
                    # Rate limiting
                    time.sleep(0.1)
        
        return all_articles
    
    def clear_cache(self):
        """Clear the cache"""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'cache_duration': self.cache_duration
        }

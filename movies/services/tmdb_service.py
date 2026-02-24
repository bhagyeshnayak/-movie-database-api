"""
TMDB Service - External API Integration
Using JSONPlaceholder as mock data for learning
"""

import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TMDBService:
    """
    Service for consuming external APIs
    Demonstrates: API patterns, error handling, caching
    """
    
    def __init__(self):
        # Using JSONPlaceholder as mock data source
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.cache: Dict[str, Dict] = {}
        self.cache_expiry: Dict[str, datetime] = {}
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.info(f"Requesting: {url}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout requesting {endpoint}")
            return {'error': 'timeout'}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return {'error': f'http_error'}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {'error': 'request_failed'}
    
    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Get data from cache if available and not expired"""
        if key in self.cache and key in self.cache_expiry:
            if datetime.now() < self.cache_expiry[key]:
                logger.info(f"Cache hit for {key}")
                return self.cache[key]
        return None
    
    def _set_in_cache(self, key: str, data: Dict, ttl: int = 3600):
        """Set data in cache with TTL (seconds)"""
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=ttl)
        logger.info(f"Cache set for {key}")
    
    def search_movies(self, query: str) -> List[Dict]:
        """
        Search movies by title (mock implementation)
        Uses JSONPlaceholder posts as mock movie data
        """
        cache_key = f"search_{query.lower()}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached.get('results', [])
        
        # Use posts endpoint as mock movie search
        params = {'q': query}
        data = self._make_request('/posts')
        
        if isinstance(data, list):
            # Transform posts into movie-like structure
            results = []
            for post in data[:10]:  # Limit to 10 results
                results.append({
                    'id': post['id'],
                    'title': post['title'],
                    'overview': post['body'][:200] + '...',
                    'release_date': '2024-01-01',
                    'vote_average': 7.5,
                    'poster_path': '/mock-poster.jpg'
                })
            
            cache_data = {'results': results}
            self._set_in_cache(cache_key, cache_data)
            return results
        
        return []
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Get detailed movie information (mock implementation)
        """
        cache_key = f"movie_{movie_id}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        # Get specific post as mock movie
        data = self._make_request(f'/posts/{movie_id}')
        
        if 'id' in data:
            movie = {
                'id': data['id'],
                'title': data['title'],
                'overview': data['body'],
                'release_date': '2024-01-01',
                'runtime': 120,
                'genres': ['Drama', 'Action'],
                'vote_average': 7.5,
                'vote_count': 100,
                'poster_path': '/mock-poster.jpg',
                'backdrop_path': '/mock-backdrop.jpg'
            }
            self._set_in_cache(cache_key, movie)
            return movie
        
        return {'error': 'Movie not found'}
    
    def get_popular_movies(self, page: int = 1) -> List[Dict]:
        """Get popular movies (mock implementation)"""
        cache_key = f"popular_{page}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached.get('results', [])
        
        params = {'_page': page, '_limit': 20}
        data = self._make_request('/posts', params)
        
        if isinstance(data, list):
            results = []
            for post in data:
                results.append({
                    'id': post['id'],
                    'title': post['title'],
                    'overview': post['body'][:150] + '...',
                    'release_date': '2024-01-01',
                    'vote_average': 7.5,
                    'poster_path': '/mock-poster.jpg'
                })
            
            cache_data = {'results': results}
            self._set_in_cache(cache_key, cache_data)
            return results
        
        return []
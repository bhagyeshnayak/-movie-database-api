"""
Test TMDB Service Integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from movies.services.tmdb_service import TMDBService

def test_tmdb_service():
    """Test basic TMDB service functionality"""
    print("🎬 Testing TMDB Service (Mock Data)...")
    print("=" * 50)
    
    service = TMDBService()
    
    # Test 1: Search movies
    print("\n1️⃣  Testing search_movies('sunt')...")
    results = service.search_movies("sunt")
    print(f"   Found {len(results)} results")
    if results:
        first = results[0]
        print(f"   First result: {first.get('title')}")
        print(f"   Overview: {first.get('overview')[:80]}...")
    
    # Test 2: Get movie details
    print("\n2️⃣  Testing get_movie_details(1)...")
    details = service.get_movie_details(1)
    if 'title' in details:
        print(f"   Title: {details['title']}")
        print(f"   Overview: {details.get('overview')[:100]}...")
        print(f"   Rating: {details.get('vote_average')}/10")
    
    # Test 3: Get popular movies
    print("\n3️⃣  Testing get_popular_movies()...")
    popular = service.get_popular_movies()
    print(f"   Found {len(popular)} popular movies")
    if popular:
        print(f"   Top movie: {popular[0].get('title')}")
    
    # Test 4: Test caching
    print("\n4️⃣  Testing cache (second call to same movie)...")
    cached_details = service.get_movie_details(1)
    if 'title' in cached_details:
        print(f"   Retrieved from cache: {cached_details['title']}")
    
    print("\n" + "=" * 50)
    print("✅ TMDB Service Tests Complete!")

if __name__ == "__main__":
    test_tmdb_service()
#!/usr/bin/env python
"""
Comprehensive test script to demonstrate all caching functionality.
"""
import os
import sys
import django
import time
import requests

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_caching_property_listings.settings')
django.setup()

from properties.models import Property
from properties.utils import get_all_properties, get_redis_cache_metrics
from django.core.cache import cache
from decimal import Decimal

def test_caching_functionality():
    """Test all caching functionality."""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("CACHING FUNCTIONALITY DEMONSTRATION")
    print("=" * 60)
    
    # 1. Test initial state
    print("\n1. INITIAL STATE:")
    print(f"Properties in database: {Property.objects.count()}")
    
    # 2. Test view-level caching
    print("\n2. VIEW-LEVEL CACHING TEST:")
    print("Making first request (should cache response for 15 minutes)...")
    response1 = requests.get(f"{base_url}/properties/")
    data1 = response1.json()
    print(f"First request - Properties count: {data1['count']}")
    
    print("Making second request (should be served from cache)...")
    response2 = requests.get(f"{base_url}/properties/")
    data2 = response2.json()
    print(f"Second request - Properties count: {data2['count']}")
    
    # 3. Test low-level caching
    print("\n3. LOW-LEVEL CACHING TEST:")
    print("Testing get_all_properties utility function...")
    
    # First call - should fetch from database and cache
    start_time = time.time()
    props1 = get_all_properties()
    time1 = time.time() - start_time
    print(f"First call - Time: {time1:.4f}s, Properties: {len(props1)}")
    
    # Second call - should be served from cache
    start_time = time.time()
    props2 = get_all_properties()
    time2 = time.time() - start_time
    print(f"Second call - Time: {time2:.4f}s, Properties: {len(props2)}")
    
    # Check if low-level cache is working
    cached_props = cache.get('all_properties')
    print(f"Low-level cache contains data: {cached_props is not None}")
    
    # 4. Test cache invalidation
    print("\n4. CACHE INVALIDATION TEST:")
    print("Adding a new property to trigger cache invalidation...")
    
    new_property = Property.objects.create(
        title='Cache Invalidation Test Property',
        description='This property tests automatic cache invalidation.',
        price=Decimal('123456.78'),
        location='Test Area'
    )
    print(f"Created property: {new_property.title}")
    
    # Check if low-level cache was invalidated
    cached_props_after = cache.get('all_properties')
    print(f"Low-level cache after invalidation: {cached_props_after is not None}")
    
    # 5. Test cache metrics
    print("\n5. CACHE METRICS:")
    metrics = get_redis_cache_metrics()
    if metrics['status'] == 'success':
        print(f"Cache Hit Ratio: {metrics['hit_ratio_percentage']}%")
        print(f"Total Requests: {metrics['total_requests']}")
        print(f"Cache Size: {metrics['cache_size']}")
        print(f"Memory Usage: {metrics['memory_usage']}")
    
    # 6. Test API endpoints
    print("\n6. API ENDPOINTS TEST:")
    
    # Properties endpoint
    response = requests.get(f"{base_url}/properties/")
    if response.status_code == 200:
        data = response.json()
        print(f"Properties API - Status: {response.status_code}, Count: {data['count']}")
    else:
        print(f"Properties API - Status: {response.status_code}")
    
    # Metrics endpoint
    response = requests.get(f"{base_url}/properties/metrics/")
    if response.status_code == 200:
        data = response.json()
        print(f"Metrics API - Status: {response.status_code}, Hit Ratio: {data.get('hit_ratio_percentage', 'N/A')}%")
    else:
        print(f"Metrics API - Status: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("CACHING DEMONSTRATION COMPLETED")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_caching_functionality()
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

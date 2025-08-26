#!/usr/bin/env python
"""
Script to test cache invalidation functionality.
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_caching_property_listings.settings')
django.setup()

from properties.models import Property
from decimal import Decimal

def test_cache_invalidation():
    """Test cache invalidation by adding a new property."""
    
    print("Testing cache invalidation...")
    
    # Add a new property
    new_property = Property.objects.create(
        title='Test Cache Invalidation Property',
        description='This property is used to test if the cache gets invalidated when a new property is added.',
        price=Decimal('999999.99'),
        location='Test Location'
    )
    
    print(f"Created new property: {new_property.title}")
    print(f"Total properties now: {Property.objects.count()}")
    
    # The cache should be automatically invalidated by the signal
    print("Cache should be automatically invalidated by Django signals")
    
    return new_property

if __name__ == '__main__':
    test_cache_invalidation()

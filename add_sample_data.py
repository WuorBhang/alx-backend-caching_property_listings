#!/usr/bin/env python
"""
Script to add sample property data for testing caching functionality.
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

def add_sample_properties():
    """Add sample properties to the database."""
    
    # Sample property data
    sample_properties = [
        {
            'title': 'Modern Downtown Apartment',
            'description': 'Beautiful 2-bedroom apartment in the heart of downtown with city views.',
            'price': Decimal('2500.00'),
            'location': 'Downtown'
        },
        {
            'title': 'Suburban Family Home',
            'description': 'Spacious 4-bedroom family home with large backyard and garage.',
            'price': Decimal('450000.00'),
            'location': 'Suburbs'
        },
        {
            'title': 'Luxury Penthouse',
            'description': 'Exclusive penthouse with panoramic views and premium amenities.',
            'price': Decimal('1200000.00'),
            'location': 'Uptown'
        },
        {
            'title': 'Cozy Studio',
            'description': 'Affordable studio apartment perfect for students or young professionals.',
            'price': Decimal('1200.00'),
            'location': 'University District'
        },
        {
            'title': 'Waterfront Condo',
            'description': 'Stunning waterfront condo with private balcony and marina access.',
            'price': Decimal('750000.00'),
            'location': 'Harbor'
        }
    ]
    
    # Add properties to database
    for prop_data in sample_properties:
        property_obj, created = Property.objects.get_or_create(
            title=prop_data['title'],
            defaults=prop_data
        )
        
        if created:
            print(f"Created: {property_obj.title} - ${property_obj.price}")
        else:
            print(f"Already exists: {property_obj.title}")
    
    print(f"\nTotal properties in database: {Property.objects.count()}")

if __name__ == '__main__':
    add_sample_properties()

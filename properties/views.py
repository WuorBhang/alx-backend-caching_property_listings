from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties, get_redis_cache_metrics


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to display all properties with view-level caching (15 minutes).
    Uses low-level caching utility for the queryset.
    """
    properties = get_all_properties()
    
    # Convert to list of dictionaries for JSON response
    property_data = []
    for prop in properties:
        property_data.append({
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat(),
        })
    
    return JsonResponse({
        'properties': property_data,
        'count': len(property_data),
        'message': 'Properties retrieved successfully'
    })


def cache_metrics(request):
    """
    View to display Redis cache performance metrics.
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)

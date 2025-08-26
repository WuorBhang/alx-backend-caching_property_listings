from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties with low-level caching.
    Cache expires after 1 hour (3600 seconds).
    """
    # Try to get from cache first
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        logger.info("Cache HIT: Retrieved properties from Redis cache")
        return cached_properties
    
    # Cache miss - fetch from database
    logger.info("Cache MISS: Fetching properties from database")
    properties = Property.objects.all()
    
    # Store in cache for 1 hour
    cache.set('all_properties', properties, 3600)
    logger.info("Stored properties in Redis cache for 1 hour")
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with cache performance data.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command output
        info = redis_conn.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Get cache size and memory usage
        cache_size = len(redis_conn.keys('*'))
        memory_usage = info.get('used_memory_human', 'N/A')
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio_percentage': round(hit_ratio, 2),
            'cache_size': cache_size,
            'memory_usage': memory_usage,
            'status': 'success'
        }
        
        # Log metrics
        logger.info(f"Cache Metrics: Hit Ratio: {hit_ratio:.2f}%, "
                   f"Hits: {keyspace_hits}, Misses: {keyspace_misses}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {str(e)}")
        return {
            'status': 'error',
            'error_message': str(e)
        }

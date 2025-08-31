import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

# Set up logging
logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties from cache if available, otherwise fetch from database.
    Caches the result for 1 hour (3600 seconds).
    """
    # Try to get properties from cache
    properties = cache.get('all_properties')
    
    # If not in cache, fetch from database and cache it
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics including hit/miss ratio.
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - hits (int): Number of successful key lookups
            - misses (int): Number of failed key lookups
            - total_operations (int): Total number of cache operations
            - hit_ratio (float): Ratio of hits to total operations (0.0 to 1.0)
            - miss_ratio (float): Ratio of misses to total operations (0.0 to 1.0)
    """
    try:
        # Get the Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis info
        info = redis_conn.info('stats')
        
        # Extract hits and misses
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        
        # Calculate hit ratio with zero division check
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        miss_ratio = 1.0 - hit_ratio if total_requests > 0 else 0
        
        metrics = {
            'hits': hits,
            'misses': misses,
            'total_operations': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'miss_ratio': round(miss_ratio, 4),
        }
        
        # Log the metrics
        logger.info(
            "Redis Cache Metrics - Hits: %s, Misses: %s, Hit Ratio: %.2f%%",
            hits, misses, hit_ratio * 100
        )
        
        return metrics
        
    except Exception as e:
        logger.error("Error retrieving Redis cache metrics: %s", str(e), exc_info=True)
        return {
            'error': str(e),
            'hits': 0,
            'misses': 0,
            'total_operations': 0,
            'hit_ratio': 0.0,
            'miss_ratio': 0.0,
        }
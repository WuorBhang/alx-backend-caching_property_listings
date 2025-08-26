from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a property is created or updated.
    """
    logger.info(f"Property {instance.title} saved - invalidating cache")
    cache.delete('all_properties')


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a property is deleted.
    """
    logger.info(f"Property {instance.title} deleted - invalidating cache")
    cache.delete('all_properties')

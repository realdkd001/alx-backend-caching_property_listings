from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Property

@receiver(post_save, sender=Property)
def invalidate_property_cache(sender, **kwargs):
    """
    Invalidate the 'all_properties' cache when a Property is saved.
    This handles both creation and updates.
    """
    cache.delete('all_properties')

@receiver(post_delete, sender=Property)
def delete_property_cache(sender, **kwargs):
    """
    Invalidate the 'all_properties' cache when a Property is deleted.
    """
    cache.delete('all_properties')
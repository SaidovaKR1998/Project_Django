from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category


def clear_product_cache():
    """
    Очистка всего кеша, связанного с продуктами
    """
    cache_keys = [
        'all_published_products',
        'all_categories_with_products',
    ]

    # Очищаем кеш категорий
    categories = Category.objects.all()
    for category in categories:
        cache.delete(f'products_category_{category.slug}')

    # Очищаем основные ключи
    for key in cache_keys:
        cache.delete(key)

    # Очищаем кеш избранных продуктов (может быть несколько вариантов)
    for i in range(1, 10):
        cache.delete(f'featured_products_{i}')


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_cache_on_product_change(sender, **kwargs):
    """
    Очистка кеша при изменении продуктов или категорий
    """
    clear_product_cache()
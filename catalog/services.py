from django.core.cache import cache
from .models import Product, Category


def get_all_published_products():
    """
    Получение всех опубликованных продуктов с кешированием
    """
    cache_key = 'all_published_products'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related('images')
        # Кешируем на 10 минут
        cache.set(cache_key, products, 60 * 10)

    return products


def get_featured_products(limit=6):
    """
    Получение избранных продуктов (например, новинки или популярные)
    """
    cache_key = f'featured_products_{limit}'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            is_published=True,
            is_featured=True  # Предполагаем, что есть такое поле
        )[:limit]
        cache.set(cache_key, products, 60 * 30)  # 30 минут

    return products

def get_products_by_category(category_slug):
    """
    Сервисная функция для получения продуктов по категории с кешированием
    """
    cache_key = f'products_category_{category_slug}'
    products = cache.get(cache_key)

    if products is None:
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(
                category=category,
                is_published=True
            ).select_related('category')
            # Кешируем на 15 минут
            cache.set(cache_key, products, 60 * 15)
        except Category.DoesNotExist:
            products = Product.objects.none()

    return products


def get_categories_with_products():
    """
    Получение всех категорий с продуктами
    """
    cache_key = 'all_categories_with_products'
    categories = cache.get(cache_key)

    if categories is None:
        categories = Category.objects.filter(
            product__is_published=True
        ).distinct().prefetch_related('product_set')
        cache.set(cache_key, categories, 60 * 15)

    return categories


def get_all_published_products():
    """
    Получение всех опубликованных продуктов с кешированием
    """
    cache_key = 'all_published_products'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(
            is_published=True
        ).select_related('category')
        # Кешируем на 10 минут
        cache.set(cache_key, products, 60 * 10)

    return products

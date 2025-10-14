from .services import get_categories_with_products

def categories_context(request):
    """
    Контекстный процессор для добавления категорий во все шаблоны
    """
    return {
        'categories': get_categories_with_products(),
    }

from django.core.cache import cache
from config.settings import CACHE_ENABLED  # Убедитесь, что переменная правильная
from catalog.models import Product

def get_products_from_cache():
    """Получает данные по товарам из кэша, если кэш пуст - получает из базы данных"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products
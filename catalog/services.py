from django.core.cache import cache
from config.settings import CACHE_ENABLED  # Убедитесь, что переменная правильная
from catalog.models import Article


def get_articles_from_cache():
    """Получает данные по статьям из кэша, если кэш пуст - получает из базы данных"""
    if not CACHE_ENABLED:
        return Article.objects.all()

    key = "articles_list"
    articles = cache.get(key)

    if articles is not None:
        return articles

    articles = Article.objects.all()
    cache.set(key, articles)

    return articles
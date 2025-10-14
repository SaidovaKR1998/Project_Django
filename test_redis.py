# test_redis.py
import os
import django
from django.core.cache import cache

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Тест кеширования
cache.set('test_key', 'test_value', 30)
result = cache.get('test_key')
print(f"Результат теста Redis: {result}")

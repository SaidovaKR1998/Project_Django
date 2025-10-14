import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache

# Тестируем кеш
cache.set('test_key', 'Работает!', 30)
result = cache.get('test_key')
print(f"✅ Результат: {result}")

# Проверяем папку кеша
import os
if os.path.exists('django_cache'):
    print("✅ Папка кеша создана")
else:
    print("❌ Папка кеша не найдена")

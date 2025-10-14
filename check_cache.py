# check_cache.py
import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.services import get_all_published_products

# Первый запрос - должен загрузить из базы
start_time = time.time()
products = get_all_published_products()
first_load = time.time() - start_time
print(f"Первый запрос: {first_load:.4f} секунд")

# Второй запрос - должен быть из кеша (быстрее)
start_time = time.time()
products = get_all_published_products()
second_load = time.time() - start_time
print(f"Второй запрос: {second_load:.4f} секунд")

print(f"Ускорение: {first_load/second_load:.2f}x")

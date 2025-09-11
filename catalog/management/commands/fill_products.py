from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполнение базы тестовыми продуктами'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        cat1 = Category.objects.create(
            name='Электроника',
            description='Электронные устройства'
        )
        cat2 = Category.objects.create(
            name='Одежда',
            description='Одежда и аксессуары'
        )

        # Создаем продукты
        products_data = [
            {
                'name': 'Ноутбук',
                'description': 'Игровой ноутбук',
                'category': cat1,
                'price': 60000
            },
            {
                'name': 'Смартфон',
                'description': 'Флагманский смартфон',
                'category': cat1,
                'price': 45000
            },
            {
                'name': 'Футболка',
                'description': 'Хлопковая футболка',
                'category': cat2,
                'price': 1500
            },
            {
                'name': 'Джинсы',
                'description': 'Классические джинсы',
                'category': cat2,
                'price': 3000
            },
        ]

        for product_data in products_data:
            Product.objects.create(**product_data)

        self.stdout.write(
            self.style.SUCCESS('База успешно заполнена тестовыми данными')
        )

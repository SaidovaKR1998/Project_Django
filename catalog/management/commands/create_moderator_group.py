from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов продуктов'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )

        # Получаем разрешения для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Безопасно получаем разрешения (создаем если нет)
        try:
            unpublish_permission = Permission.objects.get(
                codename='can_unpublish_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('⚠️ Разрешение can_unpublish_product не найдено. Создаем...')
            )
            # Создаем разрешение вручную
            unpublish_permission = Permission.objects.create(
                codename='can_unpublish_product',
                name='Может отменять публикацию продукта',
                content_type=content_type,
            )

        try:
            delete_permission = Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('⚠️ Разрешение delete_product не найдено.')
            )
            return

        # Назначаем права группе
        moderator_group.permissions.add(unpublish_permission, delete_permission)

        self.stdout.write(
            self.style.SUCCESS('✅ Группа "Модератор продуктов" создана и настроена!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✅ Назначены права: {unpublish_permission.name}, {delete_permission.name}')
        )

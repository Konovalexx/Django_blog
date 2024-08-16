import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):

    @staticmethod
    def json_read_fixtures():
        """Читаем фикстуру категорий и продуктов"""
        with open('catalog/fixtures/fixtures.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Очищаем категории и товары
        Product.objects.all().delete()
        Category.objects.all().delete()

        fixtures = Command.json_read_fixtures()

        # Сначала создаем категории
        for item in fixtures:
            if item['model'] == 'catalog.category':
                category = Category(pk=item['pk'], **item['fields'])
                category.save()

        # Затем создаем продукты, привязывая их к уже существующим категориям
        for item in fixtures:
            if item['model'] == 'catalog.product':
                category_pk = item['fields'].get('category')
                category = Category.objects.get(pk=category_pk) if category_pk else None

                product = Product(
                    pk=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description'],
                    image=item['fields'].get('image', ''),  # Используйте 'image', а не 'photo'
                    price=item['fields']['price'],
                    category=category,
                    created_at=item['fields']['created_at'],
                    updated_at=item['fields']['updated_at']
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены из fixtures.json'))
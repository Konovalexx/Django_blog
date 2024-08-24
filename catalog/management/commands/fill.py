import json
import chardet
from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ProductVersion

class Command(BaseCommand):

    @staticmethod
    def convert_to_utf8(file_path):
        """Попытка прочитать и перекодировать файл в UTF-8."""
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            detected_encoding = chardet.detect(raw_data)['encoding']

        if detected_encoding.lower() != 'utf-8':
            # Перекодируем файл в UTF-8
            decoded_data = raw_data.decode(detected_encoding)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(decoded_data)
            return True
        return False

    @staticmethod
    def json_read_fixtures():
        """Читаем фикстуру категорий и продуктов с попыткой перекодировки в UTF-8."""
        file_path = 'catalog/fixtures/fixtures.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except UnicodeDecodeError:
            # Если возникает ошибка декодирования, пытаемся перекодировать файл
            Command.convert_to_utf8(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

    def handle(self, *args, **options):
        # Очищаем категории, продукты и версии продуктов
        ProductVersion.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        fixtures = Command.json_read_fixtures()

        # Сначала создаем категории
        for item in fixtures:
            if item['model'] == 'catalog.category':
                category = Category(pk=item['pk'], **item['fields'])
                category.save()

        # Затем создаем продукты, привязывая их к уже существующим категориям
        products = {}
        for item in fixtures:
            if item['model'] == 'catalog.product':
                category_pk = item['fields'].get('category')
                category = Category.objects.get(pk=category_pk) if category_pk else None

                product = Product(
                    pk=item['pk'],
                    title=item['fields']['title'],
                    slug=item['fields']['slug'],
                    content=item['fields']['content'],
                    preview=item['fields'].get('preview', ''),
                    created_at=item['fields']['created_at'],
                    is_published=item['fields']['is_published'],
                    views_count=item['fields']['views_count'],
                    category=category,
                    price=item['fields']['price']
                )
                product.save()
                products[product.pk] = product

        # Затем создаем версии продуктов, привязывая их к уже существующим продуктам
        for item in fixtures:
            if item['model'] == 'catalog.productversion':
                product_pk = item['fields'].get('product')
                product = products.get(product_pk) if product_pk else None

                product_version = ProductVersion(
                    pk=item['pk'],
                    product=product,
                    version_number=item['fields']['version_number'],
                    version_name=item['fields']['version_name'],
                    is_current=item['fields']['is_current']
                )
                product_version.save()

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены из fixtures.json'))
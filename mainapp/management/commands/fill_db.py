from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import User
from mainapp.views import load_from_json

JSON_PATH = 'mainapp/fixtures'


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        super_user = User.objects.create_superuser('ALex', 'django@geekshop.local', 'ALex', age=21)



from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from mainapp.models import ProductCategory, Product


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self):
        cat_1 = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(100):
            Product.objects.create(
                category=cat_1,
                name=f'prod {i}'
            )
        self.client = Client()

    def test_main_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_categories_urls(self):
        for category_item in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)




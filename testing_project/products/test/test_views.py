from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from products.models import Product


class TestHomePage(SimpleTestCase):

# This test is redundant since the others look for an Http 200 by default
    # def test_homepage_status_code(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

# THIS IS AMAZING - make sure a web page contains a specific message!!!!
    def test_homepage_contains_welcome_message(self):
        response = self.client.get('/')
        self.assertContains(response, 'Welcome to our Store!')

class TestProductsPage(TestCase):
    def setUp(self):
        Product.objects.create(name='Laptop', price=1000, stock_count=5)
        Product.objects.create(name='Phone', price=800, stock_count=10)

    def test_products_uses_correct_template(self):
        # Use reverse so we target the NAMED path "products"
        # that way we aren't tried to a url called "/products/" which may change for SEO reasons
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products.html')
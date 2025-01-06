from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product(name='Test Product', price=100, stock_count=10)
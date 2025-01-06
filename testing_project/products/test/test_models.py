from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product(name='Test Product', price=100, stock_count=10)

    def test_in_stock_property(self):
        self.assertTrue(self.product.in_stock)
        # Set stock_count to 0 & test again
        self.product.stock_count = 0
        self.assertFalse(self.product.in_stock)
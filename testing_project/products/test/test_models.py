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

    def test_discount_price(self):
        self.assertEqual(self.product.get_discounted_price(10), 90)
        self.assertEqual(self.product.get_discounted_price(50), 50)
        self.assertEqual(self.product.get_discounted_price(0), 100)

    def test_negative_price_validation(self):
        self.product.price = -10
        # Make sure we get a validation error
        with self.assertRaises(ValidationError):
            # When we expect to raise the validation error
            self.product.clean()
from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product
from django.db import IntegrityError

class ProductModelTest(TestCase):
    # Create 1 object for multiple tests that won't change (better for performance)
    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name='Test Product', price=100, stock_count=10)

    def test_in_stock_property(self):
        self.assertTrue(self.product.in_stock)
        # Set stock_count to 0 & test again
        self.product.stock_count = 0
        self.assertFalse(self.product.in_stock)

    def test_discount_price(self):
        self.assertEqual(self.product.get_discounted_price(10), 90)
        self.assertEqual(self.product.get_discounted_price(50), 50)
        self.assertEqual(self.product.get_discounted_price(0), 100)

    # def test_negative_price_validation(self):
    #     self.product.price = -10
    #     # Make sure we get a validation error
    #     with self.assertRaises(ValidationError):
    #         # When we expect to raise the validation error
    #         self.product.clean()
    #
    # def test_negative_stock_count_validation(self):
    #     self.product.stock_count = -10
    #     with self.assertRaises(ValidationError):
    #         # clean validates objects, it validates the model as a whole
    #         # while clean_filed() only targets fields
    #         self.product.clean()

    def test_negative_price_constraint(self):
        product = Product(name='Negative Price Product', price=-1, stock_count=5)

        with self.assertRaises(IntegrityError):
            product.save()

    def test_negative_stock_count_constraint(self):
        product = Product(name='Negative Stock Count Product', price=1, stock_count=-1)

        with self.assertRaises(IntegrityError):
            product.save()
from django.test import TestCase
from django.urls import reverse
from products.models import Product

class ProductFormTest(TestCase):

    def test_create_product_when_submitting_valid_form(self):
        form_data = { 'name': 'Tablet', 'price': 299.99, 'stock_count': 50 }
        response = self.client.post(reverse('products'), data=form_data)

        # Check product created & we are redirected - a 302 is a redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Tablet').exists())

    def test_dont_create_product_when_submitting_invalid_form(self):
        pass
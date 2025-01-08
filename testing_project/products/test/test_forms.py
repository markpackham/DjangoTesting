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
        # This should fail, a name is required
        # Also price & stock count must not be negative
        form_data = {'name': '', 'price': -299.99, 'stock_count': -50}

        response = self.client.post(reverse('products'), data=form_data)

        # Since this fails we stay on the page and get a 200 rather than a 302 redirect
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

        form = response.context['form']
        # Error messages we expect to get
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertFormError(form, 'price', 'Price cannot be negative')
        self.assertFormError(form, 'stock_count', 'Stock count cannot be negative')

        # Make sure no product is created
        self.assertFalse(Product.objects.exists())
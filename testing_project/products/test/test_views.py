from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from products.models import Product, User

class TestProfilePage(TestCase):
     def test_profile_view_accessible_for_authenticated_users(self):
        # Create test user
        User.objects.create_user(username='testuser', password='password123')

         # Log user in
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))

        # Check user's username in the response context
        self.assertContains(response, 'testuser')


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

    def test_products_context(self):
        response = self.client.get(reverse('products'))
        # Make sure we have the 2 products we created
        self.assertEqual(len(response.context['products']), 2)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Phone')
        self.assertNotContains(response, 'No products available')

    def test_products_view_no_products(self):
        # Delete all products
        Product.objects.all().delete()
        response = self.client.get(reverse('products'))
        self.assertContains(response, 'No products available')
        self.assertEqual(len(response.context['products']), 0)

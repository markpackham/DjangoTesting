import requests
from django.test import TestCase, SimpleTestCase, tag
from django.urls import reverse
from unittest.mock import patch
from products.models import Product, User


class TestProfilePage(TestCase):
    
    # We can use tags to target specific tests that we want to run eg only "auth" tagged
    # python manage.py test --settings=testing_project.test_settings --tag=auth
    # this is a cool performance improvement
    @tag('auth')
    def test_profile_view_redirects_for_anonymous_users(self):
        response = self.client.get(reverse('profile'))
        # Check we get redirected to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    @tag('auth')
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


class PostsViewTest(TestCase):
    @patch('products.views.requests.get')
    def test_post_view_success(self, mock_get):
        mock_get.return_value.status_code = 200
        return_data = {
            "userId": 1,
            "id": 1,
            "title": "Test Title",
            "body": "Test Body"
        }
        mock_get.return_value.json.return_value = return_data

        # Send request to the view
        response = self.client.get(reverse('post'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, return_data)

        # Ensure mock API call was made with the correct Url
        mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')

        @patch('products.views.requests.get')
        def test_post_view_fail(self, mock_get):
            # We want to get a 503 error
            mock_get.side_effect = requests.exceptions.RequestException

            # Send a request to the view
            response = self.client.get(reverse('post'))

            self.assertEqual(response.status_code, 503)
            mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')

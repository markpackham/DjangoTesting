from django.test import TestCase, SimpleTestCase

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
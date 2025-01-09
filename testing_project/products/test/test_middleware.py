from django.test import TestCase
from django.urls import reverse

class MaintenanceModeTests(TestCase):

    def test_maintenance_mode_off(self):
        # Test site works normally when maintenance mode set to false
        response = self.client.get(reverse('homepage'))

        # Check response successful & normal content returned
        self.assertContains(response, 'Welcome to our Store!', status_code=200)
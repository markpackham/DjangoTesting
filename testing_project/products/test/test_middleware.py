from django.test import TestCase, override_settings
from django.urls import reverse

class MaintenanceModeTests(TestCase):

    @override_settings(MAINTENANCE_MODE=False)
    def test_maintenance_mode_off(self):
        # Test site works normally when maintenance mode set to false
        response = self.client.get(reverse('homepage'))

        # Check response successful & normal content returned
        self.assertContains(response, 'Welcome to our Store!', status_code=200)


    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_on(self):
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Site is under maintenance', status_code=503)
from django.test import TestCase
from unittest.mock import patch
from products.models import User

class UserSignalsTest(TestCase):

    # Mock functionality
    @patch('products.signals.send_mail')
    def test_welcome_email_sent_on_user_creation(self, mock_send_mail):
        # Create new user to trigger signal
        User.objects.create_user(username='john', email='john@email.com',password='password123')

        # Check send_mail called once
        mock_send_mail.assert_called_once_with(
            'Welcome!',
            'Thanks for signing up!',
            'admin@django.com',  # from-email
            ['john@email.com'],  # recipient list
            fail_silently=False,
        )

    # Check no email sent when user updated
    @patch('products.signals.send_mail')
    def test_no_email_sent_on_user_update(self, mock_send_mail):
        user = User.objects.create_user(username='john', email='john@email.com', password='password123')

        # Reset mock call count to zero
        mock_send_mail.reset_mock()
        user.email = 'johnCHANGED@email.com'
        user.save()

        mock_send_mail.assert_not_called()
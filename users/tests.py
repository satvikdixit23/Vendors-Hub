from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AuthFlowTests(TestCase):
    def test_login_view_authenticates_user_with_valid_credentials(self):
        user = CustomUser.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='secret123',
            first_name='Alice',
            phone='9876543210',
            user_type='CUSTOMER',
        )

        response = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'secret123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.pk, user.pk)

    def test_register_view_creates_customer_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'user_type': 'CUSTOMER',
            'username': 'bob',
            'phone': '9871234560',
            'email': 'bob@example.com',
            'password': 'secret123',
            'confirm_password': 'secret123',
            'full_name': 'Bob Smith',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='bob').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

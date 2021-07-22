from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from authapp.models import User
from django.core.management import call_command

from geekshop import settings


class UserManagementTestCase(TestCase):
    username = 'ALex'
    email = 'ALex@db.local'
    password = 'ALex'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username': 'django1',
        'first_name': 'django',
        'last_name': 'django',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'age': 33,
        'email': 'django1@db.local',
    }

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_user_flow(self):
        self._test_user_register()
        self._test_login()


    def _test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)
        # self.assertEqual(response.context['title'], 'главная')
        # self.assertNotContains(response, 'Пользователь', self.status_code_success)

        self.client.login(username=self.new_user_data['username'], password=self.new_user_data['password1'])

        response = self.client.get('/auth/login/')
        # self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.status_code_redirect)

    def _test_user_register(self):
        response = self.client.post('/users/login/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = User.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user.email}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', \
                     'basketapp')




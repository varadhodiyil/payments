from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from payments.auth_tokens.models import User
# Create your tests here.


class TestToken(APITestCase):
    def setUp(self):
        """
                        Create Test User
        """
        self.API_URL = reverse('login')

        params = {
            "username": "madhan_94@live.com",
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan@live.com",
            "password": "8080_1080"
        }
        url = reverse('users')
        self.client.post(url, params)

    def tearDown(self):
        User.objects.filter(username="madhan_94@live.com").delete()

    def test_valid(self):
        params = {
            'username': 'madhan_94@live.com',
            'password': '8080_1080'
        }

        response = self.client.post(self.API_URL, params)
        self.assertEqual(response.status_code, 200)

    def test_bad_params(self):
        params = {

        }
        response = self.client.post(self.API_URL, params)
        self.assertEqual(response.status_code, 400)

    def test_invalid_creds(self):
        params = {
            'username': 'madhan_94@live.com',
            'password': '8080_1080@'
        }

        response = self.client.post(self.API_URL, params)
        self.assertEqual(response.status_code, 400)

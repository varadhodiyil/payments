from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from payments.auth_tokens.models import User


class TestRegistration(APITestCase):

    def setUp(self):
        self.url = reverse('users')

    def test_register(self):
        params = {
            "username": "madhan_94@live.com",
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan@live.com",
            "password": "8080_1080"
        }

        resp = self.client.post(self.url, params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'status': True})

    def test_reregister(self):
        params = {
            "username": "madhan@live.com",
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan_94@live.com",
            "password": "8080_1080"
        }

        resp = self.client.post(self.url, params)
        self.assertEqual(resp.status_code, 200)

    def test_bad_params(self):
        params = {
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan@live.com",
            "password": "8080_1080"
        }

        resp = self.client.post(self.url, params)
        self.assertEqual(resp.status_code, 400)

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from payments.auth_tokens.models import User, Token


class Cards(APITestCase):

    def create_user(self):
        url = reverse('users')
        params = {
            "username": "madhan_94@live.com",
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan_94@live.com",
            "password": "8080_1080"
        }

        resp = self.client.post(url, params)
        self.assertEqual(resp.status_code, 200)
        self.user = User.objects.get(username="madhan_94@live.com")

    def setUp(self):
        self.create_user()

        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('get_cards')

    def test_get_cards(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_add_card_invalid(self):
        params = {
            "number": 0,
            "exp_month": 0,
            "exp_year": 0,
            "cvc": 0
        }
        url = reverse('create_card')
        resp = self.client.post(url, params)
        err_resp = {
            'status': False,
            'errors': {
                'exp_month': ['Ensure this value is greater than or equal to 1.'],
                'exp_year': ['Ensure this value is greater than or equal to 2020.']
            }
        }
        self.assertEqual(err_resp, resp.json())
        self.assertEqual(resp.status_code, 400)

    def test_add_card_valid(self):
        params = {
            "number": 4242424242424242,
            "exp_month": 10,
            "exp_year": 2021,
            "cvc": 255
        }
        url = reverse('create_card')
        resp = self.client.post(url, params)
        self.assertEqual(resp.status_code, 200)


class TestPay(APITestCase):

    def create_user(self):
        url = reverse('users')
        params = {
            "username": "madhan_94@live.com",
            "first_name": "Madhan",
            "last_name": "Mohan",
            "email": "madhan_94@live.com",
            "password": "8080_1080"
        }

        resp = self.client.post(url, params)
        self.assertEqual(resp.status_code, 200)
        self.user = User.objects.get(username="madhan_94@live.com")

    def create_card(self):
        params = {
            "number": 4242424242424242,
            "exp_month": 10,
            "exp_year": 2021,
            "cvc": 255
        }
        url = reverse('create_card')
        r = self.client.post(url, params)
        self.assertEqual(r.status_code, 200)

    def setUp(self):

        self.url = reverse('create_sub')
        self.create_user()

        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.create_card()

    def test_create_payment(self):
        params = {
            'price': 'price_1Hyh1JBjPTNvMQM4Y3qfuo6o'
        }
        resp = self.client.post(self.url, params)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'status': True})

    def test_create_payment_no_creds(self):

        _client = self.client
        params = {
            'price': 'price_1Hyh1JBjPTNvMQM4Y3qfuo6o'
        }
        _client.credentials()
        resp = _client.post(self.url, params)

        self.assertEqual(resp.status_code, 401)

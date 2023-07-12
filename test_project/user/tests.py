from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class CustomTokenObtainPairViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('token_obtain_pair')
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )

    def test_custom_token_obtain_pair_view(self):
        response = self.client.post(self.url, {'email': 'jamessmith0917topdev@gmail.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print("\nLogin check passed")


class UserSignupViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signup')

    def test_user_signup_with_valid_data(self):
        data = {
            'email': 'jamessmith0917topdev@gmail.com',
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'User created successfully'})
        print("\nSignup with valid data check passed")

    def test_user_signup_with_invalid_email(self):
        data = {
            'email': 'invalidemail',
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, [ErrorDetail(string='Enter a valid email address.', code='invalid')])
        print("\nSignup with invalid email check passed")

    def test_user_signup_with_existing_email(self):
        data = {
            'email': 'jamessmith0917topdev@gmail.com',
            'username': 'testuser',
            'password': 'testpassword'
        }
        User.objects.create_user(
            email=data['email'],
            username=data['username'],
            password=data['password']
        )
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, [ErrorDetail(string='Email already exists', code='invalid')])
        print("\nSignup with existing email check passed")

    def test_user_signup_with_missing_email(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, [ErrorDetail(string='Email is required', code='invalid')])
        print("\nSignup with missing email check passed")

class UserDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-detail')
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'testuser')
        self.assertEqual(response.data.get('email'), 'jamessmith0917topdev@gmail.com')
        print("\nUser detail view check passed")
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from time import sleep

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
REFRESH_TOKEN_URL = reverse('user:token-refresh')
ME_URL = reverse('user:me')
USERS_URL = reverse('user:users')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class PublicUserApiTests(TestCase):
    """Test that user APO (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'username': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'username': 'Test name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'pw',
            'username': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_refresh_for_user(self):
        """Test that create refresh token"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        create_user(**payload)
        access_token = self.client.post(TOKEN_URL, payload)
        sleep(1)
        res = self.client.post(REFRESH_TOKEN_URL, access_token.data)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Token is not created if invalid credentials are given"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user is not exist"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'test',
                                           'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that url ME_URL unavailable for unauthorized users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='test123',
            username='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.user.username)
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the ME_URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'username': 'new name', 'password': 'newpassword1432'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_show_all_users_for_superuser(self):
        """Test that url USERS_URL available for SuperUsers"""
        user = create_superuser(
            email='admin@gmail.com',
            password='admin',
            username='adminuser'
        )

        self.client.force_authenticate(user=user)
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_unavailable_all_users_for_user(self):
        """Test that url USERS_URL unavailable for Users"""
        user = create_user(
            email='testss@gmail.com',
            password='ssssss',
            username='name2'
        )

        self.client.force_authenticate(user=user)
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(**params):
    """Create a sample user"""
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = "test@gmail.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username='name'
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='admintest123',
            username='adminname'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_post_str(self):
        """Test the post string representation"""
        Post = models.Post.objects.create(
            user=sample_user(
                email='test@gmail.com',
                password='test123',
                username='name'
            ),
            title="Vegan"
        )
        self.assertEqual(str(Post), Post.title)

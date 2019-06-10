from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core import models

POST_URL = reverse('post:show-posts')


def sample_user(email="test@gmail.com", password='test123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class PublicPostApiTests(TestCase):
    """Test that user APO (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_unavailable_post_for_unauthorized(self):
        """Test that url POST_URL unavailable for unauthorized users"""

        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unavailable_post_detail_for_unauthorized(self):
        """Test that url POST_URL[pk] unavailable for unauthorized users"""

        post = models.Post.objects.create(
            user=sample_user(),
            title="Title1",
            content="Content1",
        )
        url = reverse("post:post-detail", kwargs={'pk': post.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unavailable_post_like_for_unauthorized(self):
        """Test that url POST_LIKE_URL unavailable for unauthorized users"""
        url = reverse('post:post-like', kwargs={'title': "Some title"})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unavailable_post_unlike_for_unauthorized(self):
        """Test that url POST_UNLIKE_URL unavailable for unauthorized users"""
        url = reverse('post:post-unlike', kwargs={'title': "Some title"})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = sample_user(
            email='test123@gmail.com',
            password='test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_methods_delete_put_patch_post(self):
        """Test that user don't delete/put/patch post on url POST_URL """
        post = models.Post.objects.create(
            user=sample_user(),
            title="Title1",
            content='Contetn',
        )

        res_delete = self.client.delete(POST_URL)
        res_put = self.client.put(POST_URL)
        res_patch = self.client.patch(POST_URL)

        self.assertEqual(res_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(res_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(res_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_method_get_post(self):
        """Test that user get post on url POST_URL """
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_method_post_for_post(self):
        """Test that user send post on url POST_URL """
        payload = {
            "title": 'Some title',
            "content": 'Some content',
        }

        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['title'], res.data['title'])
        self.assertEqual(payload['content'], res.data['content'])

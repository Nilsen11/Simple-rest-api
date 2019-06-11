from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core import models

POST_URL = reverse('post:show-posts')
CREATE_POST_URL = reverse('post:create-post')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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
            user=create_user(
                email='test@gmail.com',
                password='test123',
                name='name'
            ),
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
        self.user = create_user(
            email='test@gmail.com',
            password='test123',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = models.Post.objects.create(
            user=self.user,
            title="Some title",
            content='Content',
        )

    def test_available_post_like(self):
        """Test that url POST_LIKE_URL available for authorized users"""
        url = reverse('post:post-like', kwargs={'title': "title"})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], self.post.title)
        self.assertEqual(res.data[0]['content'], self.post.content)

    def test_available_post_unlike(self):
        """Test that url POST_UNLIKE_URL available for authorized users"""
        url = reverse('post:post-unlike', kwargs={'title': "title"})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_methods_delete_put_patch_post(self):
        """Test that user don't delete/put/patch post on url POST_URL """

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
        """Test that user create post on url CREATE_POST_URL """
        payload = {
            "title": 'Some title',
            "content": 'Some content',
        }

        res = self.client.post(CREATE_POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['title'], res.data['title'])
        self.assertEqual(payload['content'], res.data['content'])

    def test_method_put_for_post_detail(self):
        """Test that user change post details"""
        post = models.Post.objects.create(
            user=self.user,
            title="Title1",
            content='Contetn',
        )
        payload = {
            "title": 'Change title',
            'content': 'Change Content'
        }
        url = reverse("post:post-detail", kwargs={'pk': post.id})
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['content'], payload['content'])

    def test_method_get_for_post_detail(self):
        """Test that user get post details"""
        url = reverse("post:post-detail", kwargs={'pk': self.post.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.post.title)
        self.assertEqual(res.data['content'], self.post.content)

    def test_method_delete_for_post_detail(self):
        """Test that user delete post details"""
        url = reverse("post:post-detail", kwargs={'pk': self.post.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_unavailable_method_get_for_post_detail(self):
        """Test that another user can't get post"""
        post = models.Post.objects.create(
            user=create_user(
                email='AnotherUser@gmail.com',
                password='testpassword123',
                name='NewName'),
            title="Title1",
            content='Contetn'
        )

        url = reverse("post:post-detail", kwargs={'pk': post.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unavailable_method_put_for_post_detail(self):
        """Test that another user can't put post"""
        post = models.Post.objects.create(
            user=create_user(
                email='AnotherUser@gmail.com',
                password='testpassword123',
                name='NewName'),
            title="Title1",
            content='Contetn'
        )

        payload = {
            "title": 'Change title',
            'content': 'Change Content'
        }
        url = reverse("post:post-detail", kwargs={'pk': post.id})
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_unavailable_method_delete_for_post_detail(self):
        """Test that another user can't delete post"""
        post = models.Post.objects.create(
            user=create_user(
                email='AnotherUser@gmail.com',
                password='testpassword123',
                name='NewName'),
            title="Title1",
            content='Content'
        )

        url = reverse("post:post-detail", kwargs={'pk': post.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_get_for_username_post(self):
        """Test that user get on url USERNAME_POST_URL"""
        url = reverse('post:post-username', kwargs={'username': self.user.name})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)


class PrivateAdminPostApiTests(TestCase):
    """Test API requests that require authentication SuperUser"""

    def setUp(self):
        self.user = create_superuser(
            email='admin@gmail.com',
            password='admin123',
            name='AdminName'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = models.Post.objects.create(
            user=create_user(
                email='AnotherUser@gmail.com',
                password='testpassword123',
                name='NewName'),
            title="Some title",
            content='Content',
        )

    def test_unavailable_create_post_for_admin(self):
        """Test that SuperUser can't create post"""

        payload = {
            "title": 'Some title',
            "content": 'Some content',
        }
        res = self.client.post(CREATE_POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_for_admin(self):
        """Test that SuperUser can delete post"""
        url = reverse("post:post-detail", kwargs={'pk': self.post.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_post_for_admin(self):
        """Test that SuperUser can change post"""
        payload = {
            "title": 'Change title',
            'content': 'Change Content'
        }

        url = reverse("post:post-detail", kwargs={'pk': self.post.id})
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_for_admin(self):
        """Test that SuperUser can get post"""

        url = reverse("post:post-detail", kwargs={'pk': self.post.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.post.title)
        self.assertEqual(res.data['content'], self.post.content)

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Post

class PostListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('post-list')
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )

        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nPost list view check passed")

class PostCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('post-create')
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_create_view(self):
        data = {
            'text': 'Test content',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().text, 'Test content')
        print("\nPost create check passed")

class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )

        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.post = Post.objects.create(
            text='Test content',
            user=self.user
        )
        self.url = reverse('post-detail', args=[self.post.pk])

    def test_post_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nPost detail view check passed")

    def test_post_update_view(self):
        data = {
            'text': 'Updated test content'
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().text, 'Updated test content')
        print("\nPost update check passed")

    def test_post_delete_view(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        print("\nPost delete check passed")

class PostLikeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='jamessmith0917topdev@gmail.com',
            username='testuser',
            password='testpassword'
        )

        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.post = Post.objects.create(
            text='Test content',
            user=self.user
        )
        self.url = reverse('post-like', args=[self.post.pk])

    def test_post_like_view(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.likes.count(), 1)
        print("\nPost like check passed")

    def test_post_unlike_view(self):
        self.post.likes.add(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.likes.count(), 0)
        print("\nPost unlike check passed")
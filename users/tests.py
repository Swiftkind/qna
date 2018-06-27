from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .models import User
# Create your tests here.

class UserAuth(APITestCase):
    """
    Ensure we can login a user.
    """

    def test_correct_login(self):
        url = reverse('users:user_login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'test@example.com', 'password': 'sample'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_password(self):
        url = reverse('users:user_login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'test@example.com', 'password': 'adsadsa'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_exist(self):
        url = reverse('users:user_login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'notexist@example.com', 'password': 'sample'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .models import User
import unittest
from django.test import Client


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

class SimpleTestCase(unittest.TestCase):
    """Test class for user registration"""
    def setUp(self):
        self.client=Client()
        
    def test_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_errors(self):
        response = self.client.post('/users/', {
                              'email':'shem.ipanag@gmail.com',
                              'password1':'asd',
                              'password2':'a'})
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/users/', {
                              'email':'shem.ipanag@gmail.com',
                              'password1':'a',
                              'password2':'asd'})
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/users/', {
                              'email':'shem',
                              'password1':'asd',
                              'password2':'asd'})
        self.assertEqual(response.status_code, 404)

    def test_success(self):
        response = self.client.post('/users/', {
                              'email':'shem.ipanag@gmail.com',
                              'password1':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 200)

    def test_username(self):
        response = self.client.post('/users/', {
                              'email':'shem.ipanag@gmail.com',
                              'password1':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        self.client.login(username='shem.ipanag@gmail.com', password='as')

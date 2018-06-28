from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .models import User
import unittest
from django.urls import reverse
from django.test import Client


class UserLoginTest(APITestCase):
    """
    Ensure we can login a user.
    """
    def test_correct_login(self):
        url = reverse('users:login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'test@example.com', 'password': 'sample'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_password(self):
        url = reverse('users:login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'test@example.com', 'password': 'adsadsa'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_exist(self):
        url = reverse('users:login')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'notexist@example.com', 'password': 'sample'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserRegisterTest(unittest.TestCase):
    """Test class for user registration"""
    url = reverse('users:create')

    def setUp(self):
        self.client=Client()
        
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        response = self.client.post(self.url, {
                              'email':'carl.ipanag@gmail.com',
                              'password':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_errors(self):
        response = self.client.post(self.url, {
                              'email':'shem.ipanag@gmail.com',
                              'password':'asd',
                              'password2':'a',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.serializer.is_valid(), False)

        response = self.client.post(self.url, {
                              'email':'shem.ipanag@gmail.com',
                              'password':'a',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.serializer.is_valid(), False)

        response = self.client.post(self.url, {
                              'email':'shem',
                              'password':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.serializer.is_valid(), False)

    def test_success(self):
        response = self.client.post(self.url, {
                              'email':'shem.ipanag@gmail.com',
                              'password':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 201)

    def test_usernametaken(self):
        response = self.client.post(self.url, {
                              'email':'shem.ipanag@gmail.com',
                              'password':'asd',
                              'password2':'asd',
                              'first_name':'Shem',
                              'last_name':'Ipanag'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.serializer.is_valid(), False)

class UserDetailTest(APITestCase):
    """
    Test if we can get the details of a user
    """
    def test_detail_correct(self):
        url = reverse('users:details', kwargs={'handle':'test'})
        user = User.objects.create_user(email='test@example.com', password='sample')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_other_user(self):
        url = reverse('users:details', kwargs={'handle':'anotheruser'})
        user = User.objects.create_user(email='test@example.com', password='sample')
        user2 = User.objects.create_user(email='anotheruser@example.com', password='user')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_unauthorized(self):
        url = reverse('users:details', kwargs={'handle':'test'})
        user = User.objects.create_user(email='test@example.com', password='sample')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
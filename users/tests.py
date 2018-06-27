import unittest
from django.urls import reverse
from django.test import Client


class SimpleTestCase(unittest.TestCase):
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

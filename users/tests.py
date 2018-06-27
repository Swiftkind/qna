import unittest
from django.test import Client


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

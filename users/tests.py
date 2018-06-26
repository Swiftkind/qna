from django.test import TestCase
from rest_framework.test import APIClient
# Create your tests here.

client = APIClient()
client.post('/login/', {'email': 'test@example.com', 'password':'sample'}, format='json')
assert response.status_code == 200
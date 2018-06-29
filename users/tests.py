from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .models import User, Confirmation
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


class UserChangepass(APITestCase):
    """
    Test class for user changepass.
    """

    def test_get_hash(self):
        url = reverse('users:get_hash')
        user = User.objects.create_user(email='test@example.com', password='sample')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        data = {'email': 'errortest@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_check_valid(self):
        # Create a user and a unique hashed link to change password
        url = reverse('users:get_hash')
        user = User.objects.create_user(email='test@example.com',
                                        password='sample')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)

        # Setup the url
        user_query = User.objects.get(email='test@example.com')
        confirmation = Confirmation.objects.filter(user=user_query)
        url = reverse('users:changepass', args={str(confirmation[0].id)})

        # Unauthorized user uses the link
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # Authorized user uses the link
        self.client.force_authenticate(user=user)
        url = reverse('users:changepass', args={str(confirmation[0].id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Create a different user
        url = reverse('users:get_hash')
        user = User.objects.create_user(email='anothertest@example.com',
                                        password='sample')

        # Different user uses the link
        self.client.force_authenticate(user=user)
        url = reverse('users:changepass', args={str(confirmation[0].id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_changepass(self):
        # Create a user and a unique hashed link to change password
        url = reverse('users:get_hash')
        user = User.objects.create_user(email='test@example.com',
                                        password='sample')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)

        # Setup the url
        user_query = User.objects.get(email='test@example.com')
        confirmation = Confirmation.objects.filter(user=user_query)
        url = reverse('users:changepass', args={str(confirmation[0].id)})

        # Authorized user uses the link
        self.client.force_authenticate(user=user)
        url = reverse('users:changepass', args={str(confirmation[0].id)})
        response = self.client.get(url)

        # User mismatches password
        data = {'password':'asd', 'password2':'a'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        # User changes password
        data = {'password':'asd', 'password2':'asd'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        # Hash link is deleted
        self.assertEqual(len(confirmation), 0)

        # User logs in with new password
        url = reverse('users:user_login')
        data = {'email': 'test@example.com', 'password': 'asd'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class UserRegistration(APITestCase):
    """Test class for user registration"""
    url = reverse('users:create')
        
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

        # Email is taken
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

class UserEditTest(APITestCase):
    """
    Test if new data when editing a profile is valid
    """
    def test_edit_correct(self):
        url = reverse('users:details', kwargs={'handle':'test'})
        user = User.objects.create_user(
            email='test@example.com', 
            password='sample',
            first_name='Test',
            last_name='User',
            handle='test',
        )
        self.client.force_authenticate(user=user)
        data = {
            'email':'newtest@example.com',
            'first_name':'AnotherTest',
            'last_name':'AnotherUser',
            'handle':'newtest'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_changes(self):
        url = reverse('users:details', kwargs={'handle':'test'})
        user = User.objects.create_user(
            email='test@example.com', 
            password='sample',
            first_name='Test',
            last_name='User',
            handle='test',
        )
        self.client.force_authenticate(user=user)
        data = {
            'email':'test@example.com',
            'first_name':'Test',
            'last_name':'User',
            'handle':'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_exists(self):
        url = reverse('users:details', kwargs={'handle':'test'})
        user = User.objects.create_user(
            email='test@example.com', 
            password='sample',
            first_name='Test',
            last_name='User',
            handle='test',
        )
        user2 = User.objects.create_user(
            email='newtest@example.com', 
            password='sample',
            first_name='Test',
            last_name='User',
            handle='test',
        )
        self.client.force_authenticate(user=user)
        data = {
            'email':'newtest@example.com',
            'first_name':'AnotherTest',
            'last_name':'AnotherUser',
            'handle':'newtest'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
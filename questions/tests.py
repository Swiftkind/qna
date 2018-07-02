from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from users.models import User, Confirmation
from questions.models import Question, Tag, Category
from django.test import Client


class QuestionAPI(APITestCase):
    """
    Test class for QuestionAPI.
    """

    def test_list(self):
        # Setup database
        user = User.objects.create_user(email='test@example.com', password='sample')
        category = Category.objects.create(name='category')
        category.save()
        tag = Tag.objects.create(name='tag')
        tag.save()
        user_query = User.objects.get(email='test@example.com')
        confirmation = Confirmation.objects.filter(user=user_query)
        url = reverse('questions:list')
        self.client.force_authenticate(user=user)

        # Get empty list of questions
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        # Create a question
        response = self.client.post(url, {
                              'title':'sample title',
                              'content':'sample content',
                              'categories':[1],
                              'tags':[1]})
        self.assertEqual(response.status_code, 201)

        # Get non-empty list of questions
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_edit(self):
        # Setup database
        user = User.objects.create_user(email='test@example.com', password='sample')
        category = Category.objects.create(name='category')
        category.save()
        tag = Tag.objects.create(name='tag')
        tag.save()
        user_query = User.objects.get(email='test@example.com')
        confirmation = Confirmation.objects.filter(user=user_query)
        self.client.force_authenticate(user=user)

        # Create a question
        url = reverse('questions:list')
        response = self.client.post(url, {
                              'title':'sample title',
                              'content':'sample content',
                              'categories':[1],
                              'tags':[1]})
        self.assertEqual(response.status_code, 201)

        # Get question detail
        question = Question.objects.filter(user=user)
        url = reverse('questions:details', args={str(question[0].code)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)

        # Edit a question
        url = reverse('questions:details', args={str(question[0].code)})
        response = self.client.post(url, {
                              'title':'sample title',
                              'content':'sample edit content',
                              'categories':[1],
                              'tags':[1]})
        self.assertEqual(response.status_code, 201)

        # Get edited question detail
        question = Question.objects.filter(user=user)
        url = reverse('questions:details', args={str(question[0].code)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'sample edit content')        

        # Create a different user
        user = User.objects.create_user(email='anothertest@example.com',
                                        password='sample')

        # Different user uses the link
        self.client.force_authenticate(user=user)
        response = self.client.post(url, {
                              'title':'sample title',
                              'content':'sample hacked edit content',
                              'categories':[1],
                              'tags':[1]})
        self.assertEqual(response.status_code, 400)

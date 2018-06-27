from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import User
from .serializers import UserSerializer


class UsersAPI(ViewSet):
    """User API"""

    def list(self, *args, **kwargs):
        """lists all users"""
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200)

    def create(self, *args, **kwargs):
        """creates a user"""
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(serializer.errors, status=400)

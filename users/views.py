from django.shortcuts import render, redirect
from .models import User
from .serializers import UserAuthSerializer
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserSerializer


class UserAuthView(ViewSet):
    """
    User Authentication when users login
    """

    def user_list(self, *args, **kwargs):
        users = User.objects.all()
        serializer = UserAuthSerializer(users, many=True)
        return Response(serializer.data, status=200)

    def login(self, *args, **kwargs):
        serializer = UserAuthSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        login(self.request, user)
        token, created = Token.objects.get_or_create(user=user)
        context = {
            'token':token.key, 
            'log':user.last_login,
        }
        return Response(context,status=200)


class UsersAPI(ViewSet):
    """User API"""

    def list(self, *args, **kwargs):
        """lists all users"""
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200)

    def create(self, *args, **kwargs):
        """creates a user"""
        serializer = UserRegistrationSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=404)

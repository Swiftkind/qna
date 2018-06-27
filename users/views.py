from django.shortcuts import render, redirect
from .models import User
from .serializers import UserAuthSerializer
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
# Create your views here.


class UserAuthView(viewsets.ViewSet):
    """
    User Authenticaltion when users login
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

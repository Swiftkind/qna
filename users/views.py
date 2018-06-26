from django.shortcuts import render, redirect
from .models import User
from .serializers import UserAuthSerializer
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# Create your views here.


class UserAuthView(APIView):
    serializer_class = UserAuthSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(self.request, user)
            token, created = Token.objects.get_or_create(user=user)
            context = {
                'token':token.key, 
                'log':user.last_login,
            }
            return Response(context,status=200)
        else:
            return Response(serializer.errors, status=404)

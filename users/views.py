from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import (UserSerializer,
                        UserAuthSerializer,
                        ConfirmationSerializer,
                        ChangepassSerializer)
from .models import User, Confirmation


class GuestAPI(ViewSet):
    """Guest API"""

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

    def get_hash(self, *args, **kwargs):
        """submits a user email to generate confirmation"""
        serializer = ConfirmationSerializer(data=self.request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            serializer.save()
            confirmation = Confirmation.objects.filter(user=user)
            serializer = ConfirmationSerializer(confirmation, many=True)
            return Response(serializer.data, status=200)
        return Response(status=400)


class UserAPI(ViewSet):
    """Password API"""
    permission_classes = (IsAuthenticated,)
        
    def check_valid(self, *args, **kwargs):
        """returns status=200 if hashed link is valid"""
        confirmation = Confirmation.objects.get(pk=self.kwargs['hash'])
        if confirmation and confirmation.user == self.request.user:
            return Response(status=200)
        return Response(status=404)

    def details(self, *args, **kwargs):
        """view details of a user"""
        handle = self.kwargs.get('handle', None)
        instance = User.objects.get(handle=handle)
        serializer = UserDetailSerializer(instance)
        return Response(serializer.data, status=200)

    def changepass(self, *args, **kwargs):
        confirmation = Confirmation.objects.get(pk=self.kwargs['hash'])
        if confirmation and confirmation.user == self.request.user:
            serializer = ChangepassSerializer(data=self.request.data)
            if serializer.is_valid():
                serializer.save(self.request.user.id)
                return Response(status=200)
        return Response(status=400)

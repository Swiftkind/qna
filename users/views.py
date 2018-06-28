from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, UserAuthSerializer
from .models import User


class UserRegistrationAPI(ViewSet):
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

class UserAPI(ViewSet):
    """Password API"""
    permission_classes = (IsAuthenticated,)
        
    def list(self, *args, **kwargs):
        """lists all users"""
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200)

    def changepass(self, *args, **kwargs):
        pass

    def get_hash(self, *args, **kwargs):
        """lists all users"""
        pass

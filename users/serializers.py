from rest_framework import serializers
from rest_framework.compat import authenticate
from .models import User

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email Address')
    password = serializers.CharField(write_only=True)
    user = None

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        users = User.objects.filter(email=email)
        user = users.first()
        if not users or not user.check_password(password):
            raise serializers.ValidationError("Email/Password is incorrect. Please try again.")

        self.user = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer of a user"""
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']


    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        email = data['email']
        if password != password2:
            raise serializers.ValidationError("Password does not match")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def save(self):
        self.validated_data.pop('password2')
        user = User.objects.create(**self.validated_data)
        user.set_password(self.validated_data['password'])
        user.save()


class ChangepassSerializer(serializers.Serializer):
    """Serializer of a user"""
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        if password != password2:
            raise serializers.ValidationError("Password does not match")
        return data

    def save(self, id):
        user = User.objects.get(id=id)
        user.set_password(self.validated_data['password'])
        user.save()

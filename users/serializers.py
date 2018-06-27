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
            #removed  or not user.is_active in codition.. user is inactive by default
            raise serializers.ValidationError("Email/Password is incorrect. Please try again.")

        self.user = user
        return data




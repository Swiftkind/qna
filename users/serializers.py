from rest_framework import serializers 
from users.models import User


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

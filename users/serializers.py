from rest_framework import serializers
from rest_framework.compat import authenticate
from .models import User, Confirmation
from rest_framework.validators import UniqueValidator

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
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
        

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer of a user's details"""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'handle', 'date_joined']

class UserEditSerializer(serializers.Serializer):
    """Serializer when editing a user"""
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    handle = serializers.CharField(max_length=150)

    def validate(self, data):
        email = data.get('email')
        current_user = self.context['request'].user.email
        emails = User.objects.filter(email=email).exclude(email=current_user)
        # import pdb; pdb.set_trace()

        if emails.exists():
            raise serializers.ValidationError("Email already exists!")

        return data

    def save(self, handle=None):
        user = User.objects.get(handle=handle)
        user.email = self.validated_data['email']
        user.first_name = self.validated_data['first_name']
        user.last_name =  self.validated_data['last_name']
        user.handle = self.validated_data['handle']
        user.save()

class ConfirmationSerializer(serializers.ModelSerializer):
    """Serializer of a changepass confirmation"""
    email = serializers.EmailField(write_only=True)
    url = serializers.CharField(max_length=500, read_only=True)

    class Meta:
        model = Confirmation
        fields =['url', 'email']

    def validate(self, data):
        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Invalid email")
        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        self.validated_data.pop('email')
        confirmation = Confirmation.objects.create(user=user)
        confirmation.save()
        return confirmation.url


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
        confirmation = Confirmation.objects.filter(user=user).delete()

from rest_framework import serializers
from rest_framework.compat import authenticate
from .models import User

class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email Address')
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user_qs = User.objects.filter(email=email)

            if user_qs.count()==1:
                user = user_qs.first()
            else:
                raise serializers.ValidationError("This User Does Not Exist")

            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect Password")

            if not user.is_active:
                raise serializers.ValidationError("This user is no longer active")

        data['user'] = user
        return data




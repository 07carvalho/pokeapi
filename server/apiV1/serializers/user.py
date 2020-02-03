from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    This serialize will validade the registration of a new user.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'date_joined')


    def validate(self, data):
        """
        Verify if the email is used by another user
        """
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return data


class UserLoginSerializer(serializers.Serializer):
    """
    This serialize will validade a user login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': 'This user no longer exists.',
        'invalid_credentials': 'Email or password are wrong.'
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        self.user = authenticate(
                        username=data.get('username'),
                        password=data.get('password'))

        if self.user is not None:
            if self.user.is_active:
                # self.user.last_login = datetime.now()
                # self.user.save()
                return data
            raise serializers.ValidationError(self.error_messages['inactive_account'])
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token', 'created')


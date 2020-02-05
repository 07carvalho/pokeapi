from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from apiV1.serializers.user import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer


class UserRegistration(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user = User.objects.create_user(username, email, password)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLogin(generics.GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogin(generics.GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogout(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


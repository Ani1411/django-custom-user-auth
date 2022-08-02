from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserModel
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer
from users.token_handlers import token_expire_handler, expires_in


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    model = UserModel
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    model = UserModel
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
        if not user:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=status.HTTP_404_NOT_FOUND)

        user.last_login = timezone.now()
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        # token_expire_handler will check, if the token is expired it will generate new one
        is_expired, token = token_expire_handler(token)  # The implementation will be described further
        user_serialized = UserSerializer(user)
        response = {
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key
        }
        return Response(response, status=status.HTTP_200_OK)

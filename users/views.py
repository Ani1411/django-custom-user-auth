from django.contrib.auth import authenticate
# Create your views here.
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserModel
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer, PasswordSerializer
from users.token_handlers import token_expire_handler, expires_in, valid_till


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    model = UserModel
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': 'User Created Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)


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
        is_expired, token = token_expire_handler(token)

        user_serialized = UserSerializer(user)
        response = {
            'user': f"{user_serialized.data.get('first_name')} {user_serialized.data.get('last_name')}",
            'expires_in': expires_in(token),
            'valid_till': valid_till(token),
            'token': token.key,
        }

        return Response(response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Token

    def delete(self, request, *args, **kwargs):
        token = self.model.objects.get(user=request.user)
        token.delete()
        return Response({"message": 'deleted token'}, status=status.HTTP_205_RESET_CONTENT)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    model = UserModel
    serializer = UserSerializer

    def get(self, request):
        serializer = self.serializer(self.model.objects.get(id=request.user.id))
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    model = UserModel
    serializer_class = PasswordSerializer

    def put(self, request):
        user = request.user
        request.data['email'] = user.email
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

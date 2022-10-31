from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[
                                       UniqueValidator(
                                           queryset=UserModel.objects.all(),
                                           message='Email Already Exists')
                                   ])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            "email": {"error_messages": {"required": "Give yourself a email"}},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        if user := authenticate(email=attrs['email'], password=attrs['password']):
            return attrs
        raise serializers.ValidationError({"message": "Invalid Credentials or activate account"})

    class Meta:
        model = UserModel
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name", "last_login", "is_active", "date_joined",)


class PasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change.
    """
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['old_password'])
        if not user:
            raise serializers.ValidationError({"message": "old password is wrong. Enter correct password or reset it"})
        if attrs['old_password'] == attrs['password']:
            raise serializers.ValidationError({"message": "new password can't be old password"})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message": "Password fields do not match."})

        return attrs

    class Meta:
        model = UserModel
        fields = ['email', 'password', 'password2', 'old_password']

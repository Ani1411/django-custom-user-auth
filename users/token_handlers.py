from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    return timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        new_token = Token.objects.create(user=token.user)
        return is_expired, new_token
    return is_expired, token

# DEFAULT_AUTHENTICATION_CLASSES


class TokenExpiryAuthClass(TokenAuthentication):
    """
        If token is expired then it will be removed
        and new one with different key will be created
    """
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist as e:
            raise AuthenticationFailed("Invalid Token") from e
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")
        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        return token.user, token

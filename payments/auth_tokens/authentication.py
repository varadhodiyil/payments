from datetime import timedelta

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# this return left time
from payments.auth_tokens.models import Token
from django.conf import settings
from datetime import timedelta

EXPIRING_TOKEN_DURATION = getattr(
    settings, 'EXPIRING_TOKEN_DURATION', timedelta(days=1))


def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = EXPIRING_TOKEN_DURATION - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


# ________________________________________________
# DEFAULT_AUTHENTICATION_CLASSES
class TokenAuth(TokenAuthentication):
	"""
	If token is expired then it will be removed
	and new one with different key will be created
	"""
	def authenticate_credentials(self, key):
		try:
			token = Token.objects.get(key=key)
		except Token.DoesNotExist:
			print(key)
			raise AuthenticationFailed("Invalid Token")

		if not token.user.is_active:
			raise AuthenticationFailed("User is not active")

		is_expired, token = token_expire_handler(token)
		if is_expired:
			raise AuthenticationFailed("The Token is expired")

		token.expires = timezone.now() + EXPIRING_TOKEN_DURATION
		token.save()

		return token.user, token

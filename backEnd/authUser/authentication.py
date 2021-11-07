from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
import pytz


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
        self.model = self.get_model()
        try:
            token = self.model.objects.get(key=token)
        except self.model.DoesNotExist:
            return False, "Token does not exist"

        if not token.user.is_active:
            return False, "User inactive or deleted"

        # Below is implementation for token expiration
        # utc_now = datetime.utcnow()
        # utc_now = utc_now.replace(tzinfo=pytz.utc)
        #
        # if token.created < utc_now - timedelta(hours=24):
        #     raise (False, "Token has expired")

        return token.user, token


def check_auth(request_params: dict):
    tokenAuth = ExpiringTokenAuthentication()
    try:
        user, token_or_error = tokenAuth.authenticate_credentials(request_params['token_user'])
    except KeyError as e:
        return False, None, {
            'logged_in': False,
            'errors': f'BadRequest: Missing Key, {e}',
        }
    if user:
        return True, user, {
            'logged_in': True,
            'errors': ''
        }
    else:
        return False, user, {
            'logged_in': False,
            'errors': token_or_error,
        }

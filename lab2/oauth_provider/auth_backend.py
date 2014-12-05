from .models import AccessToken

class OauthBackend(object):
    def authenticate(self, *args, **kwargs):
        r, err = kwargs.get('request'), kwargs.get('err')
        if r is None or err is None: # called not from OauthMiddleware
            return None

        auth_data = r.META['HTTP_AUTHORIZATION'].split(' ')
        if len(auth_data) != 2 or auth_data[0] != 'Bearer':
            err['code'] = 'invalid_request'
            return None
        try:
            access_token = AccessToken.objects.get(value=auth_data[1])
        except AccessToken.DoesNotExist:
            print('no such token')
            err['code'] = 'invalid_token'
            return None

        if access_token.has_expired():
            print('token has expired')
            err['code'] = 'invalid_token'
            return None
        return access_token.user



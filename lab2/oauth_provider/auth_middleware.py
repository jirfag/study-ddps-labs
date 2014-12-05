from django.contrib.auth import authenticate
from django.http import JsonResponse

class OauthMiddleware(object):
    def process_request(self, r, *args, **kwargs):
        if r.user and r.user.is_authenticated(): # already logged in by non-OAuth method
            return
        if not r.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'): # not OAuth2
            return

        err_code = dict()
        user = authenticate(request=r, err=err_code)
        if user is None:
            resp = JsonResponse({'status': 'noauth'}, status=401)
            err_descs = {
                'invalid_token': 'The access token expired',
                'invalid_request': 'The request has invalid format',
            }
            err = err_code['code']
            resp['WWW-Authenticate'] = 'Bearer error="{}", error_description="{}"'.format(err, err_descs[err])
            return resp

        assert user.is_authenticated()
        r.user = user
        return None

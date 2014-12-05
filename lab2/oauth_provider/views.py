from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import ClientApp, AccessToken, RefreshToken, AuthorizationCode
from urllib.parse import urlparse

def get_params_or_404(params, *param_names):
    values = []
    for p in param_names:
        v = params.get(p)
        if v is None:
            print('no required param "{}"'.format(p))
            raise Http404
        values.append(v)
    return tuple(values) if len(values) > 1 else values[0]

@csrf_exempt
@login_required
def auth(r):
    client_id, redirect_uri, response_type = get_params_or_404(r.GET, 'client_id', 'redirect_uri', 'response_type')
    if response_type != 'code':
        return HttpResponseBadRequest()

    app = get_object_or_404(ClientApp, pk=client_id)
    if urlparse(redirect_uri).netloc != app.redirect_domain:
        print('invalid domain')
        return HttpResponseBadRequest()

    if r.method == 'GET':
        return render(r, 'oauth_provider/ask_access.html', {'app_name': app.name})

    allow = r.POST.get('allow_access')
    if allow is None:
        return HttpResponseBadRequest()

    state = '&state={}'.format(r.GET['state']) if 'state' in r.GET else ''
    if allow != '1':
        return redirect('{}?error=access_denied{}'.format(redirect_uri, state))

    code = AuthorizationCode.objects.create(app=app, user=r.user, redirect_uri=redirect_uri)
    return redirect('{}?code={}{}'.format(redirect_uri, code.value, state))

@csrf_exempt
def get_token(r):
    grant_type = get_params_or_404(r.POST, 'grant_type')
    if grant_type == 'authorization_code':
        redirect_uri, client_id, client_secret, code_value = get_params_or_404(r.POST, 'redirect_uri', 'client_id', 'client_secret', 'code')
        try:
            auth_code = AuthorizationCode.objects.get(value=code_value)
        except AuthorizationCode.DoesNotExist:
            print('no such code')
            raise Http404

        app = auth_code.app
        if int(client_id) != app.pk:
            print('invalid client_id')
            raise Http404
        if client_secret != app.secret:
            print('invalid client secret')
            raise Http404
        if redirect_uri != auth_code.redirect_uri:
            print('redirect uris dont match')
            raise Http404
        if auth_code.has_expired():
            print('auth code has expired')
            raise Http404

        access_token = AccessToken.objects.create(app=app, user=auth_code.user)
        refresh_token = RefreshToken.objects.create(app=app, user=auth_code.user)
        return JsonResponse({
            'access_token': access_token.value,
            'token_type': 'bearer',
            'expires_in': access_token.get_expiration_time(),
            'refresh_token': refresh_token.value,
        })
    else:
        print('unknown grant_type')
        raise Http404

@login_required
def index(r):
    return render(r, 'oauth_provider/index.html', {'apps': ClientApp.objects.all()})

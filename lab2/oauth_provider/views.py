from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import ClientApp, AccessToken, RefreshToken, AuthorizationCode
from urllib.parse import urlparse

def get_params_or_400(req, *param_names):
    values = []
    for p in param_names:
        v = req.GET.get(p)
        if v is None:
            raise HttpResponseBadRequest()
        values.append(v)
    return values

@require_http_methods(["GET", "POST"])
@login_required
def auth(r):
    client_id, redirect_uri, response_type = get_params_or_400(req, 'client_id', 'redirect_uri', 'response_type')
    if response_type != 'code':
        return HttpResponseBadRequest()

    app = get_object_or_404(ClientApp, pk=client_id)
    if urlparse(redirect_uri).netloc != app.redirect_domain:
        print('invalid domain')
        return HttpResponseBadRequest()

    if r.GET:
        return render_to_response('ask_access.html', {'app_name': app.name})

    allow = r.POST.get('allow_access')
    if allow is None:
        return HttpResponseBadRequest()

    state = '&state={}'.format(r.GET['state']) if 'state' in r.GET else ''
    if allow != '1':
        return redirect('{}?error=access_denied{}'.format(redirect_uri, state))

    code = AuthorizationCode.objects.create(app=app, user=r.user)
    return redirect('{}?code={}{}'.format(redirect_uri, code.value, state))

def get_token(req):
    pass

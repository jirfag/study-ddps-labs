from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import urllib3
import json
from .forms import LoginForm
from http import cookies
from .settings import SESSION_HOST, DEFAULT_AFTER_LOGIN_REDIRECT_URL

def make_api_request(url, method='GET', fields=None, headers=None):
    fields = fields or {}
    headers = headers or {}
    http = urllib3.PoolManager()
    print('API request: {} from frontend to {} with fields {} and headers {}'.format(url, method, fields, headers))

    try:
        r = http.request(method, url, headers=headers, fields=fields)
        if r:
            print('API response: status={}, headers={}, body="{}"'.format(r.status, r.getheaders(), r.data))
        return r
    except Exception as ex:
        print('exception while doing API request: {}'.format(ex))
        return None

def make_request_to_session(uri, method='GET', fields=None, headers=None):
    return make_api_request(SESSION_HOST + uri, method=method, fields=fields, headers=headers)

def check_is_authenticated(r):
    resp = make_request_to_session('/check_session', headers={'Cookie': r.META.get('HTTP_COOKIE', '')})
    if resp is None:
        print('cant make request to session')
        return None
    if resp.status != 200:
        print('session is invalid, sess status is {}'.format(resp.status))
        return False
    return True

def login_required(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        if not check_is_authenticated(r):
            return redirect('login')

        return view(r, *args, **kwargs)
    return wrapper

@login_required
def home(r):
    return render(r, 'frontend/home.html')

def morsel_to_django_cookie(m):
    r = {}
    if m['max-age']:
        r['max-age'] = float(m['max-age'])
    return r

@csrf_exempt
def login(r):
    form = LoginForm(r.POST or None)
    if r.method == 'GET':
        return render(r, 'frontend/login.html', {'form': form})
    def validate_login(data):
        resp = make_request_to_session('/authorize', method='POST', fields=data)
        if resp is None:
           print('cant make login request to session')
           return None
        if resp.status != 200:
           print('invalid username/password: status is {}, resp is {}'.format(resp.status, resp.data))
           return None
        return resp
    form._login_validator = validate_login
    if not form.is_valid():
        return render(r, 'frontend/login.html', {'form': form})

    redir_url = r.GET.get('next', DEFAULT_AFTER_LOGIN_REDIRECT_URL)
    print('redirecting to {} after successfull login'.format(redir_url))
    resp = redirect(redir_url)
    login_resp = form._login_resp
    C = cookies.SimpleCookie()
    C.load(login_resp.getheaders()['Set-Cookie'])
    for _, m in C.items():
        resp.set_cookie(m.key, m.value, **morsel_to_django_cookie(m))
    return resp

def logout(r):
    from django.contrib.auth import logout
    logout(r)
    return redirect('login')

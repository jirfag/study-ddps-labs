from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps

def api_login_required(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        if not r.user.is_authenticated():
            return {'status': 'noauth'}
        return {'status': 'ok', 'data': view(r, *args, **kwargs)}
    return wrapper

def jsonify(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        return JsonResponse(view(r, *args, **kwargs))
    return wrapper

@jsonify
@api_login_required
def me(r):
    u = r.user
    return {'name': u.first_name, 'email': u.email, 'phone': u.phone, 'username': u.username}

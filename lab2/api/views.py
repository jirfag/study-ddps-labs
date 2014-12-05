from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
from django import get_version
from accounts.models import User

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

def get_user_info(u):
    return {'name': u.first_name, 'email': u.email, 'phone': u.phone, 'username': u.username}

@jsonify
@api_login_required
def me(r):
    return get_user_info(r.user)

@jsonify
def status(r):
    return {'server': 'django', 'version': get_version(), 'users': [get_user_info(u) for u in User.objects.all()]}

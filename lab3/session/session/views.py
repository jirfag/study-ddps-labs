from .models import ClientAuthorization
from django.shortcuts import get_object_or_404, redirect, render_to_response, render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

def is_session_valid(r):
    token, user_id = r.COOKIES.get('token'), r.COOKIES.get('user_id')
    if not token or not user_id:
        print('no token and user_id in cookies')
        return None

    try:
        user_id = int(user_id)
    except ValueError:
        print('invalid user_id')
        return None

    try:
        auth = ClientAuthorization.objects.get(token=token)
    except ClientAuthorization.DoesNotExist:
        print('no authorization with such token {}'.format(token))
        return None

    if auth.has_expired():
        print('auth has expired')
        return None
    if auth.user.pk != user_id:
        print('detected malformed request of session {} for user {}'.format(token, auth.user.pk))
        return None
    print('auth with token {} and user_id {} is valid'.format(token, user_id))
    return auth.user

def check_session(r):
    user = is_session_valid(r)
    if user is not None:
        return JsonResponse({'status': 'valid', 'user': {'id': user.pk, 'name': user.first_name}})
    else:
        print('auth is invalid')
        return JsonResponse({'status': 'invalid'}, status=403)

@csrf_exempt
def authorize(r):
    username, password = r.POST['username'], r.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        print('invalid username/password: {} and {}'.format(username, password))
        return JsonResponse({'status': 'invalid'}, status=403)
    resp = JsonResponse({'status': 'valid'})
    auth = ClientAuthorization.objects.create(user=user)
    resp.set_cookie('user_id', user.pk)
    resp.set_cookie('token', auth.token)
    return resp

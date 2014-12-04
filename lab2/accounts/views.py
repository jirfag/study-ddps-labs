from django.shortcuts import render_to_response, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from oauth_provider.settings import DEFAULT_LOGIN_REDIRECT_URL
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(r):
    form = LoginForm(r.POST)
    if r.method == 'GET' or not form.is_valid():
        return render_to_response('accounts/login.html', {'form': form})

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is None:
        return render_to_response('accounts/login.html', {'form': form})

    django_login(r, user)
    return redirect(r.GET.get('next', DEFAULT_LOGIN_REDIRECT_URL))

def reg(r):
    pass

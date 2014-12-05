from django.shortcuts import render_to_response, render, redirect
from .forms import LoginForm, RegForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from oauth_provider.settings import DEFAULT_LOGIN_REDIRECT_URL, AFTER_REG_REDIRECT_URL
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt
def login(r):
    form = LoginForm(r.POST)
    if r.method == 'GET' or not form.is_valid():
        if not form.is_valid():
            print('invalid input')
        return render(r, 'accounts/login.html', {'form': form})

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is None:
        return render(r, 'accounts/login.html', {'form': form})

    django_login(r, user)
    return redirect(r.GET.get('next', DEFAULT_LOGIN_REDIRECT_URL))

@csrf_exempt
def reg(r):
    form = RegForm(r.POST)
    if r.method == 'GET' or not form.is_valid():
        if not form.is_valid():
            print('invalid input')
        return render(r, 'accounts/reg.html', {'form': form})

    data = form.cleaned_data
    try:
        User.objects.create_user(data['username'], data['email'], data['password'], first_name=data['name'], phone=data['phone'])
    except Exception as e:
        print(e)
        return render(r, 'accounts/reg.html', {'form': form})
    return redirect(AFTER_REG_REDIRECT_URL)

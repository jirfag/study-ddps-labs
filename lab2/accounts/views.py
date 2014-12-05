from django.shortcuts import render_to_response, render, redirect
from .forms import LoginForm, RegForm
from django.contrib.auth import login as django_login
from oauth_provider.settings import DEFAULT_LOGIN_REDIRECT_URL, AFTER_REG_REDIRECT_URL
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(r):
    form = LoginForm(r.POST or None)
    if r.method == 'GET':
        return render(r, 'accounts/login.html', {'form': form})
    if not form.is_valid():
        return render(r, 'accounts/login.html', {'form': form})

    django_login(r, form.user)
    redir_url = r.GET.get('next', DEFAULT_LOGIN_REDIRECT_URL)
    print('redirecting to {} after successfull login'.format(redir_url))
    return redirect(redir_url)

def logout(r):
    from django.contrib.auth import logout
    logout(r)
    return redirect('login')

@csrf_exempt
def reg(r):
    form = RegForm(r.POST or None)
    if r.method == 'GET':
        return render(r, 'accounts/reg.html', {'form': form})
    if not form.is_valid():
        return render(r, 'accounts/reg.html', {'form': form})

    django_login(r, form.user)
    return redirect(AFTER_REG_REDIRECT_URL)

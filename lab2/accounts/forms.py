from django import forms
from django.forms import PasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())

class RegForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())
    name = forms.CharField(label='Real name', max_length=128)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=16)

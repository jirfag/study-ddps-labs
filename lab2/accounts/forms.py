from django import forms
from django.forms import PasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())

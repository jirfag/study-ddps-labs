from django import forms
from django.forms import PasswordInput, ValidationError
from django.contrib.auth import authenticate
from django.db import IntegrityError

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())

    def clean(self):
        super(LoginForm, self).clean()
        self._login_resp = self._login_validator(self.cleaned_data)
        if not self._login_resp:
            raise ValidationError('Invalid username/password')

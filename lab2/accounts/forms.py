from django import forms
from django.forms import PasswordInput, ValidationError
from .models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())

    def clean(self):
        super(LoginForm, self).clean()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is None:
            raise ValidationError('Invalid username/password')
        self.user = user

class RegForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=PasswordInput())
    name = forms.CharField(label='Real name', max_length=128)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=16)

    def clean(self):
        super(RegForm, self).clean()

        data = self.cleaned_data
        try:
            User.objects.create_user(data['username'], data['email'], data['password'], first_name=data['name'], phone=data['phone'])
        except IntegrityError as e:
            raise ValidationError('Such user already exists')
        self.user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

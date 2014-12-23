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

class ImageEditForm(forms.Form):
    name = forms.CharField(label='Name', max_length=140)
    description = forms.CharField(label='Description', max_length=512)
    url = forms.URLField(label='Source')
    tags = forms.CharField(label='Tags', max_length=4096, required=False)

    @classmethod
    def from_image(cls, image):
        new_image = dict(image)
        new_image['tags'] = ','.join([t['name'] for t in image['tags']])
        return cls(new_image)

class TagEditForm(forms.Form):
    name = forms.CharField(label='Name', max_length=140)
    description = forms.CharField(label='Description', max_length=512)

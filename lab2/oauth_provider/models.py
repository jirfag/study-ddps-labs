from django.db import models
from django.contrib.auth.models import User

def generate_secret_code():
    from uuid import uuid4
    return uuid4().hex

class ClientApp(models.Model):
    name = models.CharField(max_length=512)
    secret = models.CharField(max_length=64)
    redirect_domain = models.URLField(max_length=1024)
    owner = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        self.secret = generate_secret_code()
        super(ClientApp, self).save(*args, **kwargs)

class SecretCode(models.Model):
    value = models.CharField(max_length=64, unique=True)
    app = models.ForeignKey(ClientApp)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.value = generate_secret_code()
        super(SecretCode, self).save(*args, **kwargs)

class AccessToken(SecretCode):
    pass

class RefreshToken(SecretCode):
    pass

class AuthorizationCode(SecretCode):
    pass

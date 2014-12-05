from django.db import models
from .settings import AUTH_USER_MODEL, ACCESS_TOKEN_EXPIRATION_TIME
from datetime import datetime

def generate_secret_code():
    from uuid import uuid4
    return uuid4().hex

class ClientApp(models.Model):
    name = models.CharField(max_length=512)
    secret = models.CharField(max_length=64)
    redirect_domain = models.URLField(max_length=1024)
    owner = models.ForeignKey(AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.secret = generate_secret_code()
        super(ClientApp, self).save(*args, **kwargs)

class SecretCode(models.Model):
    class Meta:
        abstract = True

    value = models.CharField(max_length=64, unique=True)
    app = models.ForeignKey(ClientApp)
    user = models.ForeignKey(AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.value = generate_secret_code()
        super(SecretCode, self).save(*args, **kwargs)

class AccessToken(SecretCode):
    def has_expired(self):
        return (datetime.now() - self.creation_date).total_seconds() >= ACCESS_TOKEN_EXPIRATION_TIME

class RefreshToken(SecretCode):
    pass

class AuthorizationCode(SecretCode):
    pass
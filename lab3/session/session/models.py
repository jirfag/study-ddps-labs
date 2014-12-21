from django.db import models
from .settings import AUTH_USER_MODEL, AUTHORIZATION_EXPIRATION_TIME
from datetime import datetime

def generate_secret_code():
    from uuid import uuid4
    return uuid4().hex

class ClientAuthorization(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    token = models.CharField(max_length=64, unique=True)
    creation_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.token = generate_secret_code()
        super(ClientAuthorization, self).save(*args, **kwargs)
    def has_expired(self):
        return (datetime.now() - self.creation_date).total_seconds() >= AUTHORIZATION_EXPIRATION_TIME

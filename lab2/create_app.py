from oauth_provider.models import ClientApp
from django.contrib.auth.models import User

ClientApp.objects.create(name='another app', redirect_domain='google.ru', owner=User.objects.all()[0])

from accounts.models import User
from oauth_provider.models import ClientApp

ClientApp.objects.all().delete()
user = User.objects.filter(username='den')[0]
ClientApp.objects.create(name='myApp', redirect_domain='mail.ru', owner=user)
ClientApp.objects.create(name='another app', redirect_domain='google.ru', owner=user)
ClientApp.objects.create(name='test app', redirect_domain='d.isaev.ru', owner=user)

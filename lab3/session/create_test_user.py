from django.contrib.auth.models import User
User.objects.all().delete()
User.objects.create_user(username='den', first_name='Denis', email='idenx@yandex.com', password='123')

from django.contrib.auth.models import User
import os

User.objects.all().delete()

user = User.objects.create_user(username='den', first_name='Denis', email='idenx@yandex.com', password='123')
print('created user {}'.format(user.pk))
cmd = r"perl -p -i -e 's/user_id1 = \d+/user_id1 = {}/g' /Users/denis/study/ddps/lab3/api_backend/fill_data.py".format(user.pk)
print(cmd)
os.system(cmd)

user = User.objects.create_user(username='test', first_name='Anton', email='anton@yandex.com', password='123')
print('created user {}'.format(user.pk))
cmd = r"perl -p -i -e 's/user_id2 = \d+/user_id2 = {}/g' /Users/denis/study/ddps/lab3/api_backend/fill_data.py".format(user.pk)
print(cmd)
os.system(cmd)

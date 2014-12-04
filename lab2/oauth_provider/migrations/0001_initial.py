# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientApp',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('secret', models.CharField(max_length=64)),
                ('redirect_domain', models.URLField(max_length=1024)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecretCode',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('value', models.CharField(max_length=64, unique=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('secretcode_ptr', models.OneToOneField(serialize=False, to='oauth_provider.SecretCode', auto_created=True, parent_link=True, primary_key=True)),
            ],
            options={
            },
            bases=('oauth_provider.secretcode',),
        ),
        migrations.CreateModel(
            name='AuthorizationCode',
            fields=[
                ('secretcode_ptr', models.OneToOneField(serialize=False, to='oauth_provider.SecretCode', auto_created=True, parent_link=True, primary_key=True)),
            ],
            options={
            },
            bases=('oauth_provider.secretcode',),
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('secretcode_ptr', models.OneToOneField(serialize=False, to='oauth_provider.SecretCode', auto_created=True, parent_link=True, primary_key=True)),
            ],
            options={
            },
            bases=('oauth_provider.secretcode',),
        ),
        migrations.AddField(
            model_name='secretcode',
            name='app',
            field=models.ForeignKey(to='oauth_provider.ClientApp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='secretcode',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

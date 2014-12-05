from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('api.views',
    url(r'^me$', 'me', name='me'),
    url(r'^status$', 'status', name='status'),
)

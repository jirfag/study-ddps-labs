from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('accounts.views',
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^reg$', 'reg', name='reg'),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'oauth_provider.views.index', name='apps_index'),
    url(r'^oauth2/auth', 'oauth_provider.views.auth', name='auth'),
    url(r'^oauth2/token', 'oauth_provider.views.get_token', name='token'),

    url(r'^accounts/', include('accounts.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oauth_provider.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^oauth2/auth', 'oauth_provider.views.auth', name='auth'),
    url(r'^oauth2/token', 'oauth_provider.views.get_token', name='token'),

    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'service_oauth.views.home', name='home'),
    url(r'^login$', 'service_oauth.views.login', name='login'),
    url(r'^logout$', 'service_oauth.views.logout', name='logout'),
    url(r'^oauth_res$', 'service_oauth.views.oauth_res', name='oauth_res'),
)

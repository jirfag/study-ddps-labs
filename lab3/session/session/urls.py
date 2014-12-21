from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'session.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^check_session$', 'session.views.check_session', name='check_session'),
    url(r'^authorize$', 'session.views.authorize', name='authorize'),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^login$', 'frontend.views.login', name='login'),
    url(r'^logout$', 'frontend.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)

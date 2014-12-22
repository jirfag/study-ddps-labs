from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^login$', 'frontend.views.login', name='login'),
    url(r'^logout$', 'frontend.views.logout', name='logout'),
    url(r'^images/all$', 'frontend.views.all_images', name='all_images'),
    url(r'^image/(?P<image_id>\d+)$', 'frontend.views.image', name='image'),
    url(r'^image/(?P<image_id>\d+)/delete$', 'frontend.views.image_delete', name='image_delete'),
    url(r'^image/(?P<image_id>\d+)/edit$', 'frontend.views.image_edit', name='image_edit'),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^login$', 'frontend.views.login', name='login'),
    url(r'^logout$', 'frontend.views.logout', name='logout'),
    url(r'^tags$', 'frontend.views.tags', name='tags'),
    url(r'^tag/(?P<tag_id>\d+)$', 'frontend.views.tag', name='tag'),
    url(r'^tag/(?P<tag_id>\d+)/edit$', 'frontend.views.tag_edit', name='tag_edit'),
    url(r'^tag/(?P<tag_id>\d+)/delete$', 'frontend.views.tag_delete', name='tag_delete'),
    url(r'^tags/create$', 'frontend.views.tag_create', name='tag_create'),
    url(r'^images/all$', 'frontend.views.all_images', name='all_images'),
    url(r'^images/my$', 'frontend.views.my_images', name='my_images'),
    url(r'^image/(?P<image_id>\d+)$', 'frontend.views.image', name='image'),
    url(r'^image/(?P<image_id>\d+)/delete$', 'frontend.views.image_delete', name='image_delete'),
    url(r'^image/(?P<image_id>\d+)/edit$', 'frontend.views.image_edit', name='image_edit'),
    url(r'^images/create$', 'frontend.views.image_create', name='image_create'),
    url(r'^admin/', include(admin.site.urls)),
)

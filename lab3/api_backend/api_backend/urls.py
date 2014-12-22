from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images$', 'api_backend.views.images', name='images'),
    url(r'^image/(?P<image_id>\d+)$', 'api_backend.views.image', name='image'),
    url(r'^tags$', 'api_backend.views.tags', name='tags'),
    url(r'^tags/(?P<tag_id>\d+)$', 'api_backend.views.tag', name='tag'),
)

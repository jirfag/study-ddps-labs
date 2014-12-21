from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images$', 'images', name='images'),
    url(r'^image/(?P<image_id>\d+)$', 'image', name='image'),
    url(r'^tags$', 'tags', name='tags'),
    url(r'^tags/(?P<tag_id>\d+)$', 'tag', name='tag'),
)

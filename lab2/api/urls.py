from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('api.views',
    url(r'^me$', 'me', name='me'),
    url(r'^status$', 'status', name='status'),
    url(r'^images$', 'images', name='images'),
    url(r'^image/(?P<image_id>\d+)$', 'image', name='image'),
    url(r'^tags$', 'tags', name='tags'),
    url(r'^tags/(?P<tag_id>\d+)$', 'tag', name='tag'),
)

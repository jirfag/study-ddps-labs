from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template import defaultfilters
from functools import wraps
from django import get_version
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from api_backend.models import Image, Tag
from .settings import IMAGES_PER_PAGE, TAGS_PER_PAGE
import json
import math

def jsonify(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        return JsonResponse(view(r, *args, **kwargs))
    return wrapper

def paginate(r, objects, objects_per_page):
    paginator = Paginator(objects, objects_per_page)
    page = r.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999)
        return []

@jsonify
@csrf_exempt
def images(r):
    if r.method == 'GET':
        f = r.GET.get('filter')
        images = Image.objects.filter(**json.loads(f)) if f else Image.objects.all()
        if r.GET.get('sort'):
            images = images.order_by(r.GET['sort'])
        c = {}
        if r.GET.get('limit'):
            images = images[:int(r.GET['limit'])]
        else: # pagination
            c['pages_count'] = math.ceil(images.count() / IMAGES_PER_PAGE)
            images = paginate(r, images, IMAGES_PER_PAGE)


        c['images'] = [{'name': im.name,
                            'id': im.pk,
                            'url': im.source
                           } for im in images]
        return c
    elif r.method == 'POST':
        try:
            req_img = r.POST #json.loads(r.body.decode('utf-8'))
        except ValueError:
            raise Http404
#        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in req_img['tags']]
        img = Image.objects.create(name=req_img['name'], desc=req_img['description'], source=req_img['url'], owner_id=req_img['owner_id'])
#        img.tags = tags
        img.save()
        return {'id': img.pk}
    else:
        print('unknown method')
        raise Http404

@jsonify
@csrf_exempt
def tags(r):
    if r.method == 'GET':
        f = r.GET.get('filter')
        tags = Tag.objects.filter(**json.loads(f)) if f else Tag.objects.all()
        if r.GET.get('sort'):
            tags = tags.order_by(r.GET['sort'])
        c = {}
        if r.GET.get('limit'):
            tags = tags[:int(r.GET['limit'])]
        else: # pagination
            c['pages_count'] = math.ceil(tags.count() / TAGS_PER_PAGE)
            tags = paginate(r, tags, TAGS_PER_PAGE)
        c['tags'] = [{'name': t.name,
                          'id': t.pk,
                          'description': t.desc
                         } for t in tags]
        return c
    elif r.method == 'POST':
        try:
            req_tag = r.POST #json.loads(r.body.decode('utf-8'))
        except ValueError as ex:
            print('ValueError: {}'.format(ex))
            raise Http404
        tag = Tag.objects.create(name=req_tag['name'], desc=req_tag['description'])
        return {'id': tag.pk}
    else:
        raise Http404

@jsonify
@csrf_exempt
def image(r, image_id):
    im = get_object_or_404(Image, pk=image_id)
    if r.method == 'GET':
        return {'name': im.name,
                'id': im.pk,
                'url': im.source,
                'description': im.desc,
                'creation_date': defaultfilters.date(im.creation_date),
                'tags': [t.pk for t in im.tags.all()]}
    elif r.method == 'DELETE':
        im.delete()
        return {}
    elif r.method == 'PUT':
        put = json.loads(r.body.decode('utf-8'))
        print('Editing image: {}'.format(put))
        im.name = put['name']
        im.desc = put['description']
        im.source = put['url']
        im.save()
        return {'status': 'ok'}
    else:
        raise Http404

@jsonify
@csrf_exempt
def tag(r, tag_id):
    t = get_object_or_404(Tag, pk=tag_id)
    if r.method == 'GET':
        return {'name': t.name,
                'id': t.pk,
                'description': t.desc,
                'creation_date': defaultfilters.date(t.creation_date),
                'images': [im.pk for im in t.image_set.all()]}
    elif r.method == 'DELETE':
        t.delete()
        return {}
    elif r.method == 'PUT':
        put = json.loads(r.body.decode('utf-8'))
        print('Editing tag: {}'.format(put))
        t.name = put['name']
        t.desc = put['description']
        t.save()
        return {'status': 'ok'}
    else:
        raise Http404

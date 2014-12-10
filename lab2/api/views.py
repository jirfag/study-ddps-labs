from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
from django import get_version
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from api.models import Image, Tag
from oauth_provider.settings import IMAGES_PER_PAGE, TAGS_PER_PAGE
import json

def api_login_required(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        if not r.user.is_authenticated():
            return {'status': 'noauth'}
        return {'status': 'ok', 'data': view(r, *args, **kwargs)}
    return wrapper

def jsonify(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        return JsonResponse(view(r, *args, **kwargs))
    return wrapper

def get_user_info(u):
    return {'name': u.first_name, 'email': u.email, 'phone': u.phone, 'username': u.username}

@jsonify
@api_login_required
def me(r):
    return get_user_info(r.user)

@jsonify
def status(r):
    return {'server': 'django', 'version': get_version(), 'users': [get_user_info(u) for u in User.objects.all()]}


# Image/Tags API

def paginate(r, objects, objects_per_page):
    paginator = Paginator(objects, objects_per_page)
    page = r.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return []

@jsonify
@api_login_required
@csrf_exempt
def images(r):
    if r.method == 'GET':
        return {'images': [{'name': im.name,
                            'id': im.pk,
                            'url': im.source
                            } for im in paginate(r, Image.objects.all(), IMAGES_PER_PAGE)]}
    elif r.method == 'POST':
        try:
            req_img = json.loads(r.body.decode('utf-8'))
        except ValueError:
            raise Http404
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in req_img['tags']]
        img = Image.objects.create(name=req_img['name'], desc=req_img['description'], source=req_img['url'])
        img.tags = tags
        img.save()
        return {'id': img.pk}
    else:
        raise Http404

@jsonify
@api_login_required
@csrf_exempt
def tags(r):
    if r.method == 'GET':
        return {'tags': [{'name': t.name,
                          'id': t.pk,
                          'description': t.desc
                         } for t in paginate(r, Tag.objects.all(), TAGS_PER_PAGE)]}
    elif r.method == 'POST':
        try:
            req_tag = json.loads(r.body.decode('utf-8'))
        except ValueError:
            raise Http404
        tag = Tag.objects.create(name=req_tag['name'], desc=req_tag['description'])
        return {'id': tag.pk}
    else:
        raise Http404

@jsonify
@api_login_required
@csrf_exempt
def image(r, image_id):
    if r.method == 'GET':
        im = get_object_or_404(Image, pk=image_id)
        return {'name': im.name,
                'id': im.pk,
                'url': im.source,
                'description': im.desc,
                'creation_date': im.creation_date,
                'tags': [t.pk for t in im.tags.all()]}
    elif r.method == 'DELETE':
        im = get_object_or_404(Image, pk=image_id)
        im.delete()
        return {}
    else:
        raise Http404

@jsonify
@api_login_required
@csrf_exempt
def tag(r, tag_id):
    if r.method == 'GET':
        t = get_object_or_404(Tag, pk=tag_id)
        return {'name': t.name,
                'id': t.pk,
                'description': t.desc,
                'creation_date': t.creation_date,
                'images': [im.pk for im in t.image_set.all()]}
    elif r.method == 'DELETE':
        t = get_object_or_404(Tag, pk=tag_id)
        t.delete()
        return {}
    else:
        raise Http404

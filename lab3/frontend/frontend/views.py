from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import urllib3
import json
from .forms import LoginForm, ImageEditForm, TagEditForm
from http import cookies
from .settings import SESSION_HOST, IMAGES_BACKEND_HOST, TAGS_BACKEND_HOST, DEFAULT_AFTER_LOGIN_REDIRECT_URL

class User(object):
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
    def is_authenticated(self):
        return True

class AnonymousUser(User):
    def __init__(self):
        super(AnonymousUser, self).__init__(None, None)
    def is_authenticated(self):
        return False

def make_api_request(url, method='GET', fields=None, headers=None):
    fields = fields or {}
    headers = headers or {}
    http = urllib3.PoolManager()
    print('API request: addr="{}", method={}, fields="{}", headers="{}"'.format(url, method, fields, headers))

    try:
        if method == 'PUT':
            r = http.urlopen(method, url, headers=headers, body=json.dumps(fields))
        else:
            r = http.request(method, url, headers=headers, fields=fields)
        if r:
            print('API response: status={}, headers={}, body="{}"'.format(r.status, r.getheaders(), r.data))
        return r
    except Exception as ex:
        import traceback
        traceback.print_exc()
        print('exception while doing API request: {}'.format(ex))
        return None

def make_request_to_session(uri, **kwargs):
    return make_api_request(SESSION_HOST + uri, **kwargs)

def make_request_to_images_backend(uri, **kwargs):
    resp = make_api_request(IMAGES_BACKEND_HOST + uri, **kwargs)
    if resp is None:
        return None
    return json.loads(resp.data.decode('utf-8'))

def make_request_to_tags_backend(uri, **kwargs):
    resp = make_api_request(TAGS_BACKEND_HOST + uri, **kwargs)
    if resp is None:
        return None
    return json.loads(resp.data.decode('utf-8'))

def check_is_authenticated(r):
    resp = make_request_to_session('/session/check', headers={'Cookie': r.META.get('HTTP_COOKIE', '')})
    r._user = AnonymousUser()
    if resp is None:
        print('cant make request to session')
        return False
    if resp.status != 200:
        print('session is invalid, sess status is {}'.format(resp.status))
        return False
    udata = json.loads(resp.data.decode('utf-8'))['user']
    r._user = User(udata['id'], udata['name'])
    return True

def check_auth(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        check_is_authenticated(r)
        return view(r, *args, **kwargs)
    return wrapper

def login_required(view):
    @wraps(view)
    def wrapper(r, *args, **kwargs):
        if not r._user.is_authenticated():
            return redirect('login')
        return view(r, *args, **kwargs)
    return wrapper

@check_auth
def home(r):
    return render(r, 'frontend/home.html', {'user': r._user})

def morsel_to_django_cookie(m):
    r = {}
    if m['max-age']:
        r['max-age'] = float(m['max-age'])
    return r

@check_auth
def login(r):
    form = LoginForm(r.POST or None)
    if r.method == 'GET':
        return render(r, 'frontend/login.html', {'form': form, 'user': r._user})
    def validate_login(data):
        resp = make_request_to_session('/authorize', method='POST', fields=data)
        if resp is None:
           print('cant make login request to session')
           return None
        if resp.status != 200:
           print('invalid username/password: status is {}, resp is {}'.format(resp.status, resp.data))
           return None
        return resp
    form._login_validator = validate_login
    if not form.is_valid():
        return render(r, 'frontend/login.html', {'form': form, 'user': r._user})

    redir_url = r.GET.get('next', DEFAULT_AFTER_LOGIN_REDIRECT_URL)
    print('redirecting to {} after successfull login'.format(redir_url))
    resp = redirect(redir_url)
    login_resp = form._login_resp
    C = cookies.SimpleCookie()
    C.load(login_resp.getheaders()['Set-Cookie'])
    for _, m in C.items():
        resp.set_cookie(m.key, m.value, **morsel_to_django_cookie(m))
    return resp

def logout(r):
    make_request_to_session('/session/delete', method='DELETE', headers={'Cookie': r.META.get('HTTP_COOKIE', '')})
    return redirect('home')

@check_auth
def all_images(r):
    page = int(r.GET.get('page', '1'))
    resp = make_request_to_images_backend('/images', fields={'page': page})
    c = {'images': resp['images'], 'pages_count': resp['pages_count'], 'page': page, 'user': r._user, 'page_name': 'all_images'}
    print('context is {}'.format(c))
    return render(r, 'frontend/images_list.html', c)

@check_auth
@login_required
def my_images(r):
    page = int(r.GET.get('page', '1'))
    fields = {
                'page': page,
                'filter': json.dumps({
                    'owner_id': r._user.user_id
                })
             }
    resp = make_request_to_images_backend('/images', fields=fields)
    c = {'images': resp['images'], 'pages_count': resp['pages_count'], 'page': page, 'user': r._user, 'page_name': 'my_images'}
    print('context is {}'.format(c))
    return render(r, 'frontend/images_list.html', c)

def get_image_by_id(image_id):
    image = make_request_to_images_backend('/image/{}'.format(image_id))
    if image['tags']:
        fields = {'filter': json.dumps({'id__in': image['tags']})}
        all_tags = make_request_to_tags_backend('/tags', fields=fields)['tags']
        all_tags_dict = {tag['id']: tag for tag in all_tags}
        image['tags'] = [all_tags_dict[tag_id] for tag_id in image['tags']]
    return image

@check_auth
def image(r, image_id):
    image = get_image_by_id(image_id)
    return render(r, 'frontend/image.html', {'image': image, 'user': r._user})

@check_auth
@login_required
def image_delete(r, image_id):
    make_request_to_images_backend('/image/{}'.format(image_id), method='DELETE')
    return redirect('all_images')

@check_auth
@login_required
def image_edit(r, image_id):
    if r.method == 'GET':
        image = get_image_by_id(image_id)
        form = ImageEditForm.from_image(image)
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})
    form = ImageEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})

    req = dict(form.cleaned_data)
    needed_tag_names = req['tags'].split(',')
    req['tags'] = []
    existing_tags = make_request_to_tags_backend('/tags', fields={'filter': json.dumps({'name__in': needed_tag_names})})['tags']
    existing_tags_dict = {t['name']: t for t in existing_tags}
    for tname in needed_tag_names:
        if tname in existing_tags_dict:
            tag = existing_tags_dict[tname]
        else:
            tag = make_request_to_tags_backend('/tags', method='POST', fields={'name': tname, 'description': ''})
        req['tags'].append(tag['id'])

    make_request_to_images_backend('/image/{}'.format(image_id), method='PUT', fields=req)
    return redirect('image', image_id=image_id)

@check_auth
@login_required
def image_create(r):
    if r.method == 'GET':
        form = ImageEditForm()
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})
    form = ImageEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})

    req = dict(form.cleaned_data)
    req['owner_id'] = r._user.user_id

    needed_tag_names = req['tags'].split(',')
    req['tags'] = []
    existing_tags = make_request_to_tags_backend('/tags', fields={'filter': json.dumps({'name__in': needed_tag_names})})['tags']
    existing_tags_dict = {t['name']: t for t in existing_tags}
    for tname in needed_tag_names:
        if tname in existing_tags_dict:
            tag = existing_tags_dict[tname]
        else:
            tag = make_request_to_tags_backend('/tags', method='POST', fields={'name': tname, 'description': ''})
        req['tags'].append(tag['id'])
    req['tags'] = json.dumps(req['tags'])
    img = make_request_to_images_backend('/images', method='POST', fields=req)
    print('create image {} from req {}'.format(img, req))
    return redirect('image', image_id=img['id'])

@check_auth
def tags(r):
    page = int(r.GET.get('page', '1'))
    resp = make_request_to_tags_backend('/tags', fields={'page': page})
    return render(r, 'frontend/tags_list.html', {'tags': resp['tags'], 'page': page, 'pages_count': resp['pages_count'], 'user': r._user})

@check_auth
def tag(r, tag_id):
    t = make_request_to_tags_backend('/tag/{}'.format(tag_id))
    fields = {
        'filter': json.dumps({'tags__id': t['id']}),
        'sort': '-creation_date',
        'limit': 3
    }
    last_images_with_tag = make_request_to_images_backend('/images', fields=fields)['images']
    return render(r, 'frontend/tag.html', {'tag': t, 'images': last_images_with_tag, 'user': r._user})

@check_auth
@login_required
def tag_create(r):
    if r.method == 'GET':
        form = TagEditForm()
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})
    form = TagEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})

    tag = make_request_to_tags_backend('/tags', method='POST', fields=form.cleaned_data)
    return redirect('tag', tag_id=tag['id'])

@check_auth
@login_required
def tag_edit(r, tag_id):
    if r.method == 'GET':
        tag = make_request_to_tags_backend('/tag/{}'.format(tag_id))
        form = TagEditForm(tag)
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})
    form = TagEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/form_edit.html', {'form': form, 'user': r._user})

    make_request_to_tags_backend('/tag/{}'.format(tag_id), method='PUT', fields=form.cleaned_data)
    return redirect('tag', tag_id=tag_id)

@check_auth
@login_required
def tag_delete(r, tag_id):
    make_request_to_tags_backend('/tag/{}'.format(tag_id), method='DELETE')
    return redirect('tags')

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import urllib3
import json
from .forms import LoginForm, ImageEditForm
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
            r = http.urlopen(method, url, header=headers, body=json.dumps(fields))
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
    c = {'images': resp['images'], 'pages_count': resp['pages_count'], 'page': page, 'user': r._user}
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
    c = {'images': resp['images'], 'pages_count': resp['pages_count'], 'page': page, 'user': r._user}
    print('context is {}'.format(c))
    return render(r, 'frontend/images_list.html', c)

def get_image_by_id(image_id):
    image = make_request_to_images_backend('/image/{}'.format(image_id))
    if image['tags']:
        fields = {'filter': json.dumps({'pk__in': image['tags']})}
        all_tags = make_request_to_tags_backend('/tags', fields=fields)['tags']
        all_tags_dict = {tag['id']: tag for tag in all_tags}
        image['tags'] = [all_tags_dict[tag_id] for tag_id in image['tags']]
    return image

@check_auth
def image(r, image_id):
    image = get_image_by_id(image_id)
    return render(r, 'frontend/image.html', {'image': image, 'user': r._user})

def image_delete(r, image_id):
    make_request_to_images_backend('/image/{}'.format(image_id), method='DELETE')
    return redirect('all_images')

@check_auth
def image_edit(r, image_id):
    if r.method == 'GET':
        image = get_image_by_id(image_id)
        form = ImageEditForm.from_image(image)
        return render(r, 'frontend/image_edit.html', {'form': form, 'user': r._user})
    form = ImageEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/image_edit.html', {'form': form, 'user': r._user})

    make_request_to_images_backend('/image/{}'.format(image_id), method='PUT', fields=form.cleaned_data)
    return redirect('/image/{}'.format(image_id))

@check_auth
@login_required
def image_create(r):
    if r.method == 'GET':
        form = ImageEditForm()
        return render(r, 'frontend/image_edit.html', {'form': form, 'user': r._user})
    form = ImageEditForm(r.POST)
    if not form.is_valid():
        return render(r, 'frontend/image_edit.html', {'form': form, 'user': r._user})

    req = dict(form.cleaned_data)
    req['owner_id'] = r._user.user_id
    image = make_request_to_images_backend('/images', method='POST', fields=req)
    return redirect('/image/{}'.format(image['id']))

@check_auth
def tags(r):
    page = int(r.GET.get('page', '1'))
    resp = make_request_to_tags_backend('/tags', fields={'page': page})
    return render(r, 'frontend/tags_list.html', {'tags': resp['tags'], 'page': page, 'pages_count': resp['pages_count'], 'user': r._user})

@check_auth
@login_required
def tag_create(r):
    pass

@check_auth
def tag(r, tag_id):
    t = make_request_to_tags_backend('/tags/{}'.format(tag_id))
    return render(r, 'frontend/tag.html', {'tag': t, 'user': r._user})

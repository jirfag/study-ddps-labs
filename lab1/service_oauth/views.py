from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render_to_response
from service_oauth.settings import SERVICE_OAUTH_CONFIG, FULL_HOST_NAME, SERVICE_HOST
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
import urllib3
import json

def make_api_request(page, method='GET', fields=None, headers=None):
    fields = fields or {}
    headers = headers or {}

    http = urllib3.PoolManager()
    url = SERVICE_HOST + page
    r = http.request(method, url, headers=headers, fields=fields)
    resp = r.data.decode('utf-8')
    print('resp is %s' % resp)
    return json.loads(resp)

def get_user_images(req):
    headers = {'Authorization': 'Bearer {0}'.format(req.session['oauth_access_token'])}
    resp = make_api_request('/3/account/idenx/images/0', headers=headers)
    print('headers: %s, response: %s' % (headers, resp))
    return [i['link'] for i in resp['data']]

def home(req):
    if 'oauth_access_token' not in req.session:
        return redirect('login')

    print('oauth_access_token is %s' % req.session['oauth_access_token'])
    user_images = get_user_images(req)
    print('user images are %s' % user_images)
    return render_to_response('home.html', {'images': user_images})

def oauth_res(req):
    if 'code' not in req.GET:
        return HttpResponseBadRequest()

    print('got oauth code %s' % req.GET['code'])
    fields = {'client_id': SERVICE_OAUTH_CONFIG['client_id'], 'client_secret': SERVICE_OAUTH_CONFIG['client_secret'],
            'grant_type': 'authorization_code', 'code': req.GET['code']}
    resp = make_api_request('/oauth2/token', 'POST', fields=fields)
    req.session['oauth_access_token'] = resp['access_token']
    return redirect('home')

def logout(req):
    del req.session['oauth_access_token']
    print('logout...')
    return redirect('home')

def login(req):
    return do_oauth_authorization(req)

def do_oauth_authorization(req):
    return_url = FULL_HOST_NAME + reverse('oauth_res')
    oauth_url_fmt = SERVICE_HOST + '/oauth2/authorize?client_id={0}&response_type=code&state=state1'
    oauth_url = oauth_url_fmt.format(SERVICE_OAUTH_CONFIG['client_id'])
    print('redirecting to %s' % oauth_url)
    return redirect(oauth_url)

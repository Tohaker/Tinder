'''
Refactored from  https://github.com/philipperemy/Deep-Learning-Tinder/blob/master/tinder_token.py

Custom method: `get_facebook_id`
'''
import re

import requests
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import robobrowser

MOBILE_USER_AGENT = 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)'
FACEBOOK_AUTH = 'https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd'
COOKIE = {'datr': 'QPfMYSxhry4rroXCVDe4_geS'}

def get_facebook_access_token(email, password):
    '''
    Gets Facebook access token using email and password.

    :param email: Facebook username: email.
    :param password: Facebook password.
    '''
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser='lxml')
    s.session.cookies.update(COOKIE)
    s.open(FACEBOOK_AUTH)

    f = s.get_form()
    f['pass'] = password
    f['email'] = email
    s.submit_form(f)
    f = s.get_form()

    try:
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'], allow_redirects=False)
        access_token = re.search(
            r"access_token=([\w\d]+)", s.response.headers['Location']).groups()[0]
        return access_token
    except Exception as ex:
        return {'error': 'access token could not be retrieved. Check your username and password.', 'exception': str(ex)}


def get_facebook_id(access_token):
    '''
    Gets facebook ID from access token

    :param access_token: most likely obtained from :method: `get_facebook_access_token`
    '''
    if 'error' in access_token:
        return {'error': 'access token could not be retrieved'}
    req = requests.get(
        'https://graph.facebook.com/me?access_token=' + access_token)
    return req.json()['id']

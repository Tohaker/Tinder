from tinder_api import Tinder_API
from tinder_api import helpers as api_helpers
from tinder_api import facebook_auth_token
import getpass


class Tests(object):
    def __init__(self, *args):
        self._tinder_api = Tinder_API()


    def test_auth(self):
        input_valid = False
        while input_valid == False:
            fb_or_sms = input('Do you want to authenticate with Facebook or SMS? [fb/sms]\n')
            input_valid = fb_or_sms in ['fb', 'sms']
        if fb_or_sms == 'sms':
            phone_number = input('What is your phone number?\n')
            self._tinder_api.send_otp_code(phone_number)
            refresh_token = self._tinder_api.get_refresh_token(phone_number, input('Please enter the code you received by SMS\n'))
            api_token = self._tinder_api.get_api_token(refresh_token)
        else:
            facebook_username = input('What is your Facebook username?\n')
            facebook_password = getpass.getpass()
            facebook_access_token = facebook_auth_token.get_facebook_access_token(facebook_username, facebook_password)
            api_token = self._tinder_api.get_facebook_auth_token(facebook_access_token)
        print("Your api token is '{api_token}'. Please make a note of it.\n".format(api_token=api_token))


    def authenticate(self, api_token):
        self._tinder_api.authenticate(api_token)

    
    def test_routes(self):
        recs = self._tinder_api.get_recs_v2()
        if recs['meta']['status'] != 200:
            print('get_recs_v2 failed')
        api_helpers.pause()

        updates = self._tinder_api.get_updates(last_activity_date='2020-05-21T17:00:00.392Z')
        if updates['last_activity_date'] == '':
            print('get_updates failed')
        api_helpers.pause()

        profile = self._tinder_api.get_self()
        if len(profile.keys()) == 0:
            print('get_self failed')
        api_helpers.pause()

        meta = self._tinder_api.get_meta()
        if meta['status'] != 200:
            print('get_meta failed')
        api_helpers.pause()

        meta2 = self._tinder_api.get_meta_v2()
        if meta2['meta']['status'] != 200:
            print('get_meta_v2 failed')
        api_helpers.pause()

        user = self._tinder_api.get_person(profile['_id'])
        if user['status'] != 200:
            print('get_person failed')
        api_helpers.pause()

        matches = self._tinder_api.matches(limit=1)
        first_match_id = matches['data']['matches'][0]['_id']
        if matches['meta']['status'] != 200:
            print('matches failed')
        api_helpers.pause()

        match = self._tinder_api.get_match(first_match_id)
        if match['meta']['status'] != 200 or first_match_id != match['data']['_id']:
            print('get_match failed')
        api_helpers.pause()

        like_result = self._tinder_api.like(match['data']['person']['_id'])
        if like_result['status'] != 200:
            print('like failed')
        api_helpers.pause()

        like_count = self._tinder_api.fast_match_count()
        if like_count['meta']['status'] != 200:
            print('fast_match_count failed')
        api_helpers.pause()

        teasers = self._tinder_api.fast_match_teasers()
        if teasers['meta']['status'] != 200:
            print('fast_match_teasers failed')
        api_helpers.pause()

        gifs = self._tinder_api.gif_query('hi', limit=1)
        if gifs['meta']['status'] != 200:
            print('gif_query failed')
        api_helpers.pause()

        gifs = self._tinder_api.trending_gifs(limit=1)


# END CLASS


testing_suite = Tests()

valid_input = False
while valid_input == False:
    user_input = input('Test authentication? [y/n]\n')
    valid_input = user_input in ['y', 'n']
if user_input == 'y':
    testing_suite.test_auth()
else:
    testing_suite.authenticate(input('What is your api_token? (no quotes)\n'))
testing_suite.test_routes()
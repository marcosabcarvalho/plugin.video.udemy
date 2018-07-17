import requests

from matthuisman.util import process_brightcove, log
from matthuisman.exceptions import LoginError

from . import config

class API(object):
    def __init__(self, addon):
        self._addon = addon

        self._session = requests.session()
        self._session.headers.update(config.HEADERS)

        access_token = self._addon.data.get('access_token')
        if access_token:
            self._set_auth(access_token)

        self._logged_in = access_token != None

    def _set_auth(self, access_token):
        self._session.headers.update({'Authorization': 'Bearer {0}'.format(access_token)})

    @property
    def logged_in(self):
        return self._logged_in

    def my_courses(self):
        params = {
            'page_size': 1000,
            'ordering': '-access_time,-enrolled',
            'fields[course]': '@min,image_750x422,headline',
        }

        return self._session.get(config.BASE_API.format('/users/me/subscribed-courses'), params=params).json()

    def login(self, username, password):
        resp = self._session.get(config.LOGIN_URL)

        payload = {
            "email": username,
            "password": password,
            "csrfmiddlewaretoken": resp.cookies.get('csrftoken'),
            'locale': 'en_US',
        }
        params = {'response_type': 'json'}

        resp = self._session.post(config.LOGIN_URL, params=params, data=payload)
        access_token = resp.cookies.get('access_token')
        if not access_token:
            self._addon.data.pop('access_token', None)
            self._logged_in = False
            raise LoginError("Failed to login. Check your details are correct and try again.")

        self._set_auth(access_token)
        self._addon.data['access_token'] = access_token
        self._logged_in = True
import re
from collections import OrderedDict

from matthuisman.controller import Controller as BaseController
from matthuisman.exceptions import InputError, ViewError

from .api import API
from . import config

class Controller(BaseController):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self._api = API(self._addon)

    def home(self, params):
        items = [
            {'title':'My Courses', 'url': self._router.get(self.my_courses)},
        ]

        if not self._api.logged_in:
            items.append({'title':'[B]Login[/B]', 'url': self._router.get(self.login)})
        else:
            items.append({'title':'Logout', 'url': self._router.get(self.logout)})

        items.append({'title':'Settings', 'url': self._router.get(self.settings)})

        self._view.items(items, cache=False)

    def _require_login(self):
        if not self._api.logged_in:
            self._do_login()

    def my_courses(self, params):
        self._require_login()

        func = lambda: self._api.my_courses()['results']
        if self._addon.settings.getBool('use_cache'):
            data = self._addon.cache.function('my_courses', func, expires=config.MY_COURSES_EXPIRY)
        else:
            data = func()

        items = []
        for course in data:
            plot = '{}\n\n{} Lectures ({})\n{}% Complete'.format(self._strip_tags(course['headline'].encode('utf-8').strip()), course['num_published_lectures'], course['content_info'], course['completion_ratio'])

            items.append({
                'title': course['title'],
                'images': {'thumb': course['image_480x270']},
                'info': {'plot': plot},
                'url': self._router.get(self.course, {'id': course['id']})
            })

        self._view.items(items, title='My Courses')

    def _strip_tags(self, text):
        return re.sub('<[^>]*>', '', text)

    def course(self, params):
        self._require_login()

        func = lambda: self._api.course_items(params['id'])['results']

        if self._addon.settings.getBool('use_cache'):
            data = self._addon.cache.function('course_{}'.format(params['id']), func, expires=config.COURSE_EXPIRY)
        else:
            data = func()

        items = []
        _title = params.get('title')
        for item in data:
            if item['_class'] == 'chapter':
                items.append({
                    'title': '~ [B]Section {}: {}[/B] ~'.format(item['object_index'], item['title']),
                    'info': {'plot': self._strip_tags(item['description'])},
                    'images': {'thumb': item['course']['image_480x270']},
                })
                print(item)
                _title = item['course']['title']
            elif item['_class'] == 'lecture' and item['is_published'] and item['asset']['asset_type'] in ('Video', 'Audio'):
                items.append({
                    'title': item['title'],
                    'info': {'plot': self._strip_tags(item['description']), 'duration': item['asset']['length']},
                    'images': {'thumb': item['thumbnail_url']},
                    'url': self._router.get(self.play, {'id': item['asset']['id']}),
                    'playable': True,
                })

        self._view.items(items, title=_title)

    def play(self, params):
        self._require_login()

        use_ia_hls = self._addon.settings.getBool('use_ia_hls')
        data       = self._api.get_asset(params['id'])
        streams    = data.get('stream_urls', {}).get('Video') or stream_urls.get('Audio')

        if not streams:
            raise ViewError('No streams found')

        urls = []
        for item in streams:
            if item['type'] == 'application/x-mpegURL':
                urls.append([item['file'], 'hls', use_ia_hls])
            else:
                urls.append([item['file'], item['type'], int(item['label'])])

        urls = sorted(urls, key=lambda x: (x[2] is True, x[2]), reverse=True)
        url, _type = urls[0][0:2]
   
        item = {
            'url': url,
            'vid_type': _type,
            'options': {'use_ia_hls': use_ia_hls},
        }

        self._view.play(item)

    def login(self, params):
        self._do_login()

    def logout(self, params):
        if not self._view.dialog_yes_no("Are you sure you want to logout?"):
            raise InputError()

        self._api.logout()

    def _do_login(self):
        username = self._view.get_input("Udemy Email", default=self._addon.data.get('username', '')).strip()
        if not username:
            raise InputError()

        password = self._view.get_input("Udemy Password", hidden=True).strip()
        if not password:
            raise InputError()

        self._addon.data['username'] = username
        self._api.login(username=username, password=password)
import re
import os
from collections import OrderedDict

from matthuisman.controller import Controller as BaseController
from matthuisman.exceptions import InputError, ViewError
from matthuisman.view import Item
from matthuisman.util import clean_s
from matthuisman.addon import __addon_path__

from . import config
from .api import API

class Controller(BaseController):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self._api = API(self._addon)

    def home(self, params):
        items = [
            Item(label='My Courses', art=True, path=self._router.get(self.my_courses), is_folder=True)
        ]

        if not self._api.logged_in:
            items.append(Item(label='[B]Login[/B]', art=True, path=self._router.get(self.login)))
        else:
            items.append(Item(label='Logout', art=True, path=self._router.get(self.logout)))

        items.append(Item(label='Settings', art=True, path=self._router.get(self.settings)))

        self._view.items(items, cacheToDisc=False)

    def my_courses(self, params):
        self._require_login()

        data = self._addon.cache.function(
            key     = 'my_courses', 
            func    = lambda: self._api.my_courses()['results'],
            expires = config.MY_COURSES_EXPIRY, 
            fresh   = not self._addon.settings.getBool('use_cache')
        )

        items = []
        for course in data:
            plot = '{}\n\n{} Lectures ({})\n{}% Complete'.format(self._strip_tags(course['headline'].encode('utf-8').strip()), course['num_published_lectures'], course['content_info'], course['completion_ratio'])

            item = Item(
                label     = course['title'],
                path      = self._router.get(self.course, {'id': course['id']}),
                art       = {'thumb': course['image_480x270']},
                info      = {'plot': plot},
                is_folder = True,
            )
            items.append(item)

        self._view.items(items, title='My Courses')

    def _strip_tags(self, text):
        return re.sub('<[^>]*>', '', clean_s(text))

    def course(self, params):
        self._require_login()

        data = self._addon.cache.function(
            key      = 'course_{}'.format(params['id']), 
            func     = lambda: self._api.course_items(params['id'])['results'], 
            expires  = config.COURSE_EXPIRY, 
            fresh    = not self._addon.settings.getBool('use_cache')
        )

        items = []
        _title = None

        for row in data:
            if row['_class'] == 'chapter':
                _title = row['course']['title']

                item = Item(
                    label = '~ [B]Section {}: {}[/B] ~'.format(row['object_index'], row['title']),
                    art   = {'thumb': row['course']['image_480x270']},
                    info  = {'plot': self._strip_tags(row['description'])},
                )
                items.append(item)

            elif row['_class'] == 'lecture' and row['is_published'] and row['asset']['asset_type'] in ('Video', 'Audio'):
                item = Item(
                    label = row['title'], path=self._router.get(self.play, {'id': row['asset']['id']}),
                    art   = {'thumb': row['course']['image_480x270']},
                    info  = {
                        'plot': self._strip_tags(row['description']), 
                        'duration': row['asset']['length'],
                        'playcount': int(row['progress_status'] == 'started' and row['last_watched_second'] == 0),
                    },
                    playable = True,
                )
                items.append(item)

        self._view.items(items, title=_title)

    def logout(self, params):
        if not self._view.dialog_yes_no("Are you sure you want to logout?"):
            raise InputError()

        self._api.logout()
        self._view.refresh()
        
    def login(self, params):
        self._do_login()
        self._view.refresh()

    def _require_login(self):
        if not self._api.logged_in:
            self._do_login()

    def _do_login(self):
        username = self._view.get_input("Udemy Email", default=self._addon.data.get('username', '')).strip()
        if not username:
            raise InputError()

        password = self._view.get_input("Udemy Password", hidden=True).strip()
        if not password:
            raise InputError()

        self._addon.data['username'] = username
        self._api.login(username=username, password=password)

    def play(self, params):
        self._require_login()

        data       = self._api.get_asset(params['id'])
        streams    = data.get('stream_urls', {}).get('Video') or stream_urls.get('Audio')
        use_ia_hls = self._addon.settings.getBool('use_ia_hls')

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

        item = Item(path=url)
        if use_ia_hls and _type == 'hls':
            item.set_ia_hls()

        self._view.play(item)
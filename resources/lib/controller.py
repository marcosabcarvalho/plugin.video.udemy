from collections import OrderedDict

from matthuisman.controller import Controller as BaseController
from matthuisman.exceptions import InputError

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

        self._view.items(items)

    def my_courses(self, params):
        if not self._api.logged_in:
            self._do_login()

        func = lambda: self._api.my_courses()
        data = self._addon.cache.function('my_courses', func, expires=config.COURSES_EXPIRY)

        items = []
        for course in data['results']:
            items.append({
                'title': course['title'],
                'images': {'thumb': course['image_750x422']},
                'info': {'plot': course['headline']},
                'url': self._router.get(self.lectures, {'course_id': course['id']})
            })

        self._view.items(items, title='My Courses')

    def lectures(self, params):
        pass
    
    def login(self, params):
        self._do_login()
        self._view.refresh()

    def logout(self, params):
        if not self._view.dialog_yes_no("Are you sure you want to logout?"):
            raise InputError()

        self._api.logout()
        self._view.refresh()

    def _do_login(self):
        username = self._view.get_input("Udemy Email", default=self._addon.data.get('username', '')).strip()
        if not username:
            raise InputError()

        password = self._view.get_input("Udemy Password", hidden=True).strip()
        if not password:
            raise InputError()

        self._addon.data['username'] = username
        self._api.login(username=username, password=password)
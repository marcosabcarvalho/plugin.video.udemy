from matthuisman import userdata
from matthuisman.session import Session
from matthuisman.log import log

from .constants import HEADERS, API_URL

class API(object):
    def new_session(self):
        self.logged_in = False
        self._session = Session(HEADERS, base_url=API_URL)
        self.set_access_token(userdata.get('access_token'))

    def set_access_token(self, token):
        if token:
            self._session.headers.update({'Authorization': 'Bearer {0}'.format(token)})
            self.logged_in = True

    def my_courses(self):
        log('API: My Courses')

        params = {
            'page_size'       : 9999,
            'ordering'        : '-access_time,-enrolled',
            'fields[course]'  : 'id,title,image_480x270,image_750x422,headline,num_published_lectures,content_info,completion_ratio',
        }

        return self._session.get('users/me/subscribed-courses', params=params).json()['results']

    def course_items(self, course_id):
        log('API: Course Items')

        params = {
            'page_size'        : 9999,
            'fields[course]'   : 'title,image_480x270',
            'fields[chapter]'  : 'description,object_index,title,course',
            'fields[lecture]'  : 'title,object_index,description,is_published,created,progress_status,last_watched_second,course,asset',
            'fields[asset]'    : 'asset_type,length,status',
            'fields[practice]' : 'id',
            'fields[quiz]'     : 'id',
        }

        return self._session.get('courses/{}/cached-subscriber-curriculum-items'.format(course_id), params=params).json()['results']

    def get_stream_urls(self, asset_id):
        params = {
            'fields[asset]'   : '@min,status,stream_urls,length,course',
        }

        return self._session.get('assets/{0}'.format(asset_id), params=params).json().get('stream_urls', {})

    def login(self, username, password):
        log('API: Login')

        data = {
            "email": username,
            "password": password
        }

        params = {
            'fields[user]': 'title,image_100x100,name,access_token',
        }

        data = self._session.post('auth/udemy-auth/login/', params=params, data=data).json()
        access_token = data.get('access_token')
        
        if not access_token:
            self.logout()
            error = data.get('detail', '')
            raise Exception(error)

        userdata.set('access_token', access_token)
        self.set_access_token(access_token)

    def logout(self):
        log('API: Logout')
        userdata.delete('access_token')
        self.new_session()
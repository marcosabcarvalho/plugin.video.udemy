import re

from HTMLParser import HTMLParser

from matthuisman import plugin, gui, cache, settings, userdata, inputstream
from matthuisman.util import get_string as _
from matthuisman.log import log

from .api import API
from .constants import MY_COURSES_EXPIRY, COURSE_EXPIRY

L_LOGIN            = 30000
L_MY_COURSES       = 30001
L_LOGOUT           = 30002
L_SETTINGS         = 30003
L_ASK_USERNAME     = 30004
L_ASK_PASSWORD     = 30005
L_LOGIN_ERROR      = 30006
L_LOGOUT_YES_NO    = 30007
L_COURSE_INFO      = 30008
L_SECTION_LABEL    = 30009
L_NO_STREAM_ERROR  = 30010

h = HTMLParser()
def strip_tags(text):
    if not text:
        return ''

    text = re.sub('\([^\)]*\)', '', text)
    text = re.sub('<[^>]*>', '', text)
    text = h.unescape(text)
    return text

api = API()

@plugin.before_dispatch()
def before_dispatch():
    api.new_session()
    plugin.logged_in = api.logged_in
    cache.enabled    = settings.getBool('use_cache', True)

@plugin.route('')
def home():
    folder = plugin.Folder()

    if not api.logged_in:
        folder.add_item(label=_(L_LOGIN), path=plugin.url_for(login))
    else:
        folder.add_item(label=_(L_MY_COURSES), path=plugin.url_for(my_courses), cache_key=cache.key_for(my_courses))
        folder.add_item(label=_(L_LOGOUT), path=plugin.url_for(logout))

    folder.add_item(label=_(L_SETTINGS), path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def login():
    while not api.logged_in:
        username = gui.input(_(L_ASK_USERNAME), default=userdata.get('username', '')).strip()
        if not username:
            break

        userdata.set('username', username)

        password = gui.input(_(L_ASK_PASSWORD), default=cache.get('password', '')).strip()
        if not password:
            break

        cache.set('password', password, expires=60)

        try:
            api.login(username=username, password=password)
        except Exception as e:
            gui.ok(_(L_LOGIN_ERROR, error_msg=e))

    cache.delete('password')

@plugin.route()
def logout():
    if not gui.yes_no(_(L_LOGOUT_YES_NO)):
        return

    api.logout()

@plugin.route()
@plugin.login_required()
@cache.cached(MY_COURSES_EXPIRY)
def my_courses():
    folder = plugin.Folder(title=_(L_MY_COURSES))

    for row in api.my_courses():
        plot = _(L_COURSE_INFO, 
            title            = row['headline'], 
            num_lectures     = row['num_published_lectures'], 
            percent_complete = row['completion_ratio'],
            length           = row['content_info'],
        )

        folder.add_item(
            label     = row['title'],
            path      = plugin.url_for(course, course_id=row['id']),
            cache_key = cache.key_for(course, course_id=row['id']),
            art       = {'thumb': row['image_480x270']},
            info      = {'plot': plot},
            is_folder = True,
        )

    return folder

@plugin.route()
@plugin.login_required()
@cache.cached(COURSE_EXPIRY)
def course(course_id):
    folder = plugin.Folder()

    for row in api.course_items(course_id):
        if row['_class'] == 'chapter':
            folder.title = row['course']['title']

            folder.add_item(
                label = _(L_SECTION_LABEL, section_number=row['object_index'], section_title=row['title']),
                art   = {'thumb': row['course']['image_480x270']},
                info  = {'plot':  strip_tags(row['description'])},
                is_folder = False,
            )

        elif row['_class'] == 'lecture' and row['is_published'] and row['asset']['asset_type'] in ('Video', 'Audio'):
            folder.add_item(
                label = row['title'], 
                path = plugin.url_for(play, asset_id=row['asset']['id']),
                art   = {'thumb': row['course']['image_480x270']},
                info  = {
                    'plot':      strip_tags(row['description']), 
                    'duration':  row['asset']['length'],
                    'playcount': int(row['progress_status'] == 'started' and row['last_watched_second'] == 0),
                    'mediatype': 'episode',
                },
                playable = True,
            )

    return folder

@plugin.route()
@plugin.login_required()
def play(asset_id):
    use_ia_hls  = settings.getBool('use_ia_hls')
    quality     = int(settings.get('max_quality').strip('p'))

    stream_urls = api.get_stream_urls(asset_id)
    streams     = stream_urls.get('Video') or stream_urls.get('Audio') or []

    urls = []
    for item in streams:
        if item['type'] != 'application/x-mpegURL':
            urls.append([item['file'], int(item['label'])])
        elif use_ia_hls:
            return plugin.PlayerItem(inputstream=inputstream.HLS(), path=item['file'])
    
    if not urls:
        raise plugin.Error(_(L_NO_STREAM_ERROR))

    urls = sorted(urls, key=lambda x: x[1], reverse=True)
    for url in urls:
        if url[1] <= quality:
            return plugin.PlayerItem(path=url[0])

    return plugin.PlayerItem(path=urls[-1][0])
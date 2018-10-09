import re

from HTMLParser import HTMLParser

from matthuisman import plugin, gui, cache, settings, userdata, inputstream, signals
from matthuisman.log import log

from .api import API
from .constants import MY_COURSES_EXPIRY, COURSE_EXPIRY
from .language import _

h = HTMLParser()
def strip_tags(text):
    if not text:
        return ''

    text = re.sub('\([^\)]*\)', '', text)
    text = re.sub('<[^>]*>', '', text)
    text = h.unescape(text)
    return text

api = API()

@signals.on(signals.BEFORE_DISPATCH)
def before_dispatch():
    api.new_session()
    plugin.logged_in = api.logged_in

@plugin.route('')
def home():
    folder = plugin.Folder()

    if not api.logged_in:
        folder.add_item(label=_(_.LOGIN, _bold=True), path=plugin.url_for(login))
    else:
        folder.add_item(label=_(_.MY_COURSES, _bold=True), path=plugin.url_for(my_courses), cache_key=cache.key_for(my_courses))
        folder.add_item(label=_.LOGOUT, path=plugin.url_for(logout))

    folder.add_item(label=_.SETTINGS, path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def login():
    while not api.logged_in:
        username = gui.input(_.ASK_USERNAME, default=userdata.get('username', '')).strip()
        if not username:
            break

        userdata.set('username', username)

        password = gui.input(_.ASK_PASSWORD, default=cache.get('password', '')).strip()
        if not password:
            break

        cache.set('password', password, expires=60)

        try:
            api.login(username=username, password=password)
        except Exception as e:
            gui.ok(_(_.LOGIN_ERROR, error_msg=e))

    cache.delete('password')
    gui.refresh()

@plugin.route()
def logout():
    if not gui.yes_no(_.LOGOUT_YES_NO):
        return

    cache.empty()
    api.logout()
    gui.refresh()

@plugin.route()
@plugin.login_required()
@cache.cached(MY_COURSES_EXPIRY)
def my_courses():
    folder = plugin.Folder(title=_.MY_COURSES)

    for row in api.my_courses():
        plot = _(_.COURSE_INFO, 
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

    if not folder.items:
        folder.add_item(
            label = _(_.NO_COURSES, _label=True),
            is_folder = False,
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
                label = _(_.SECTION_LABEL, section_number=row['object_index'], section_title=row['title']),
                art   = {'thumb': row['course']['image_480x270']},
                info  = {'plot':  strip_tags(row['description'])},
                is_folder = False,
            )

        elif row['_class'] == 'lecture' and row['is_published'] and row['asset']['asset_type'] in ('Video', 'Audio'):
            folder.add_item(
                label = row['title'], 
                path  = plugin.url_for(play, asset_id=row['asset']['id']),
                art   = {'thumb': row['course']['image_480x270']},
                info  = {
                    'title':      row['title'],
                    'plot':       strip_tags(row['description']), 
                    'duration':   row['asset']['length'],
                    'mediatype':  'episode',
                    'tvshowtitle': row['course']['title'],
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
            return plugin.Item(inputstream=inputstream.HLS(), path=item['file'], art=False)
    
    if not urls:
        raise plugin.Error(_.NO_STREAM_ERROR)

    urls = sorted(urls, key=lambda x: x[1], reverse=True)
    for url in urls:
        if url[1] <= quality:
            return plugin.Item(path=url[0], art=False)

    return plugin.Item(path=urls[-1][0], art=False)
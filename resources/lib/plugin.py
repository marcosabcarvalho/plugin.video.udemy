from matthuisman import plugin, gui, settings, userdata, inputstream, signals
from matthuisman.log import log

from .api import API
from .language import _

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
        _my_courses(folder)
        folder.add_item(label=_.LOGOUT, path=plugin.url_for(logout))

    folder.add_item(label=_.SETTINGS, path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def login():
    username = gui.input(_.ASK_USERNAME, default=userdata.get('username', '')).strip()
    if not username:
        return

    userdata.set('username', username)

    password = gui.input(_.ASK_PASSWORD, hide_input=True).strip()
    if not password:
        return

    api.login(username=username, password=password)
    gui.refresh()

@plugin.route()
def logout():
    if not gui.yes_no(_.LOGOUT_YES_NO):
        return

    api.logout()
    gui.refresh()

def _my_courses(folder):
    for row in api.my_courses():
        plot = _(_.COURSE_INFO, 
            title            = row['headline'], 
            num_lectures     = row['num_published_lectures'], 
            percent_complete = row['completion_ratio'],
            length           = row['content_info'],
        )

        folder.add_item(
            label     = row['title'],
            path      = plugin.url_for(chapters, course_id=row['id']),
            art       = {'thumb': row['image_480x270']},
            info      = {'plot': plot},
            is_folder = True,
        )

    if not folder.items:
        folder.add_item(
            label = _(_.NO_COURSES, _label=True),
            is_folder = False,
        )

@plugin.route()
def chapters(course_id):
    course = api.course(course_id)
    folder = plugin.Folder(title=course['title'])

    for chapter_id, chapter in sorted(course['chapters'].iteritems(), key=lambda (k,v): v['index']):
        folder.add_item(
            label     = _(_.SECTION_LABEL, section_number=chapter['index'], section_title=chapter['title']),
            path      = plugin.url_for(lectures, course_id=course_id, chapter_id=chapter_id),
            art       = {'thumb': course['image']},
            info      = {'plot': chapter['description']},
        )

    return folder

@plugin.route()
def lectures(course_id, chapter_id):
    course = api.course(course_id)
    chapter = course['chapters'][int(chapter_id)]

    folder = plugin.Folder(title=chapter['title'])

    for lecture in chapter['lectures']:
        folder.add_item(
            label = lecture['title'], 
            path  = plugin.url_for(play, asset_id=lecture['asset']['id']),
            art   = {'thumb': course['image']},
            info  = {
                'title':      lecture['title'],
                'plot':       lecture['description'], 
                'duration':   lecture['asset']['length'],
                'mediatype':  'episode',
                'tvshowtitle': course['title'],
            },
            playable = True,
        )

    return folder

@plugin.route()
@plugin.login_required()
def play(asset_id):
    use_ia_hls  = settings.getBool('use_ia_hls')
    quality     = int(settings.get('max_quality', '1080p').strip('p'))

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
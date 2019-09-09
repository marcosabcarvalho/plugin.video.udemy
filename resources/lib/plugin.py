import re

from HTMLParser import HTMLParser

from matthuisman import plugin, gui, settings, userdata, inputstream, signals
from matthuisman.log import log
from matthuisman.constants import QUALITY_TAG

from .api import API
from .language import _
from .constants import QUALITY_OPTIONS, QUALITY_BEST, QUALITY_LOWEST, QUALITY_ASK

api = API()

@signals.on(signals.BEFORE_DISPATCH)
def before_dispatch():
    api.new_session()
    plugin.logged_in = api.logged_in

@plugin.route('')
def home(**kwargs):
    folder = plugin.Folder()

    if not api.logged_in:
        folder.add_item(label=_(_.LOGIN, _bold=True), path=plugin.url_for(login))
    else:
        folder.add_item(label=_(_.MY_COURSES, _bold=True), path=plugin.url_for(my_courses))
        folder.add_item(label=_.LOGOUT, path=plugin.url_for(logout))

    folder.add_item(label=_.SETTINGS, path=plugin.url_for(plugin.ROUTE_SETTINGS))

    return folder

@plugin.route()
def login(**kwargs):
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
def logout(**kwargs):
    if not gui.yes_no(_.LOGOUT_YES_NO):
        return

    api.logout()
    gui.refresh()

@plugin.route()
def my_courses(page=1, **kwargs):
    page   = int(page)
    folder = plugin.Folder(title=_.MY_COURSES)

    data = api.my_courses(page=page)

    for row in data['results']:
        plot = _(_.COURSE_INFO, 
            title            = row['headline'], 
            num_lectures     = row['num_published_lectures'], 
            percent_complete = row['completion_ratio'],
            length           = row['content_info'],
        )

        folder.add_item(
            label     = row['title'],
            path      = plugin.url_for(chapters, course_id=row['id'], title=row['title']),
            art       = {'thumb': row['image_480x270']},
            info      = {'plot': plot},
            is_folder = True,
        )

    if not folder.items:
        folder.add_item(
            label = _(_.NO_COURSES, _label=True),
            is_folder = False,
        )

    if data['next']:
        folder.add_item(
            label = _(_.NEXT_PAGE, _bold=True),
            path  = plugin.url_for(my_courses, page=page+1),
        )

    return folder

@plugin.route()
def chapters(course_id, title, page=1, **kwargs):
    page   = int(page)
    folder = plugin.Folder(title=title)

    rows, next_page = api.chapters(course_id, page=page)

    for row in sorted(rows, key=lambda r: r['object_index']):
        folder.add_item(
            label     = _(_.SECTION_LABEL, section_number=row['object_index'], section_title=row['title']),
            path      = plugin.url_for(lectures, course_id=course_id, chapter_id=row['id'], title=title),
            art       = {'thumb': row['course']['image_480x270']},
            info      = {'plot': strip_tags(row['description'])},
        )

    if next_page:
        folder.add_item(
            label = _(_.NEXT_PAGE, _bold=True),
            path  = plugin.url_for(chapters, course_id=course_id, title=title, page=page+1),
        )

    return folder

@plugin.route()
def lectures(course_id, chapter_id, title, page=1, **kwargs):
    page    = int(page)
    folder = plugin.Folder(title=title)

    rows, next_page = api.lectures(course_id, chapter_id, page=page)

    for row in rows:
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

    if next_page:
        folder.add_item(
            label = _(_.NEXT_PAGE, _bold=True),
            path  = plugin.url_for(lectures, course_id=course_id, chapter_id=chapter_id, title=title, page=page+1),
        )

    return folder

@plugin.route()
@plugin.login_required()
def play(asset_id, **kwargs):
    use_ia_hls  = settings.getBool('use_ia_hls')
    stream_urls = api.get_stream_urls(asset_id)
    streams     = stream_urls.get('Video') or stream_urls.get('Audio') or []

    urls = []
    for item in streams:
        if item['type'] != 'application/x-mpegURL':
            urls.append([item['file'], int(item['label'])])
        else:
            return plugin.Item(path=item['file'], art=False, inputstream=inputstream.HLS())
    
    if not urls:
        raise plugin.Error(_.NO_STREAM_ERROR)

    urls = sorted(urls, key=lambda x: x[1], reverse=True)

    if not settings.getBool('quality_enabled'):
        return plugin.Item(path=urls[0][0], art=False)

    quality = settings.getEnum('mp4_quality', QUALITY_OPTIONS, default=QUALITY_BEST)

    if quality == QUALITY_ASK or kwargs.get(QUALITY_TAG):
        options = [QUALITY_BEST]
        labels  = [_.QUALITY_BEST]

        for url in urls:
            options.append(url[1])
            labels.append('{}P'.format(url[1]))

        options.append(QUALITY_LOWEST)
        labels.append(_.QUALITY_LOWEST)

        index = gui.select(_.SELECT_QUALITY, labels)
        if index < 0:
            return

        quality = options[index]

    if quality == QUALITY_BEST:
        selected = urls[0]
    elif quality == QUALITY_LOWEST:
        selected = urls[-1]
    else:
        selected = urls[-1]

        for url in urls:
            if url[1] <= quality:
                selected = url
                break

    return plugin.Item(path=selected[0], art=False)

h = HTMLParser()
def strip_tags(text):
    if not text:
        return ''

    text = re.sub('\([^\)]*\)', '', text)
    text = re.sub('<[^>]*>', '', text)
    text = h.unescape(text)
    return text
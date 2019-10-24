import json
from threading import Thread
from six.moves.urllib_parse import urlparse

from kodi_six import xbmc

from . import userdata, gui, router, inputstream, settings
from .language import _
from .constants import QUALITY_TYPES, QUALITY_ASK, QUALITY_BEST, QUALITY_CUSTOM, QUALITY_SKIP, QUALITY_LOWEST, QUALITY_TAG, QUALITY_DISABLED, ADDON_DEV
from .log import log
from .parser import M3U8, MPD, ParserError

def select_quality(qualities):
    options = []

    options.append([QUALITY_BEST, _.QUALITY_BEST])
    options.extend(qualities)
    options.append([QUALITY_LOWEST, _.QUALITY_LOWEST])
    options.append([QUALITY_SKIP, _.QUALITY_SKIP])

    values = [x[0] for x in options]
    labels = [x[1] for x in options]

    current = userdata.get('last_quality')

    default = 0
    if current:
        try:
            default = values.index(current)
        except:
            default = values.index(qualities[-1][0])

            for quality in qualities:
                if quality[0] <= current:
                    default = values.index(quality[0])
                    break
                
    index = gui.select(_.PLAYBACK_QUALITY, labels, preselect=default)
    if index < 0:
        return None

    userdata.set('last_quality', values[index])

    return values[index]

def reset_thread(reset_func):
    log.debug('Settings Reset Thread: STARTED')

    monitor    = xbmc.Monitor()
    player     = xbmc.Player()
    sleep_time = 100#ms

    #wait upto 3 seconds for playback to start
    count = 0
    while not monitor.abortRequested():
        if player.isPlaying():
            break

        if count > 3*(1000/sleep_time):
            break

        count += 1
        xbmc.sleep(sleep_time)

    #wait upto 30 seconds for playback to start
    count = 0
    while not monitor.abortRequested():
        if not player.isPlaying() or player.getTime() > 0:
            break

        if count > 30*(1000/sleep_time):
            break

        count += 1
        xbmc.sleep(sleep_time)

    reset_func()

    log.debug('Settings Reset Thread: DONE')

def get_gui_settings(keys):
    settings = {}

    for key in keys:
        try:
            value = json.loads(xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{{"setting":"{}"}}, "id":1}}'.format(key)))['result']['value']
            settings[key] = value
        except:
            pass
        
    return settings

def set_gui_settings(settings):
    for key in settings:
        xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{{"setting":"{}", "value":{}}}, "id":1}}'.format(key, settings[key]))

def set_settings(min_bandwidth, max_bandwidth, is_ia=False):
    reset_func = None

    if is_ia:
        new_ia_settings = {
            'MINBANDWIDTH':        min_bandwidth,
            'MAXBANDWIDTH':        max_bandwidth,
            'IGNOREDISPLAY':       'true',
            'HDCPOVERRIDE':        'true',
            'STREAMSELECTION':     '0',
            'MEDIATYPE':           '0',
            'MAXRESOLUTION':       '0',
            'MAXRESOLUTIONSECURE': '0',
        }

        inputstream.set_bandwidth_bin(1000000000) #1000m/bit

        current_ia_settings = inputstream.get_settings(new_ia_settings.keys())
        if new_ia_settings != current_ia_settings:
            inputstream.set_settings(new_ia_settings)
            reset_func = lambda: inputstream.set_settings(current_ia_settings)
    else:
        new_gui_settings = {
            'network.bandwidth': int(max_bandwidth/1000),
        }

        current_gui_settings = get_gui_settings(new_gui_settings.keys())
        if new_gui_settings != current_gui_settings:
            set_gui_settings(new_gui_settings)
            reset_func = lambda: set_gui_settings(current_gui_settings)

    if reset_func and not ADDON_DEV:
        thread = Thread(target=reset_thread, args=(reset_func,))
        thread.daemon = True
        thread.start()

def get_quality():
    return settings.getEnum('default_quality', QUALITY_TYPES, default=QUALITY_ASK)

def add_context(item):
    if item.playable and get_quality() != QUALITY_DISABLED:
        url = router.add_url_args(item.path, **{QUALITY_TAG: QUALITY_ASK})
        item.context.append((_.PLAYBACK_QUALITY, 'XBMC.PlayMedia({})'.format(url)))

def parse(item, quality=None):
    if quality is None:
        quality = get_quality()
        if quality == QUALITY_CUSTOM:
            quality = int(settings.getFloat('max_bandwidth')*1000000)
    else:
        quality = int(quality)

    if quality in (QUALITY_DISABLED, QUALITY_SKIP):
        return

    url   = item.path.split('|')[0]
    parse = urlparse(url.lower())
    
    if 'http' not in parse.scheme:
        return

    parser = None
    if item.inputstream and item.inputstream.check():
        is_ia = True
        if item.inputstream.manifest_type == 'mpd':
            parser = MPD()
        elif item.inputstream.manifest_type == 'hls':
            parser = M3U8()
    else:
        is_ia = False
        if parse.path.endswith('.m3u') or parse.path.endswith('.m3u8'):
            parser = M3U8()
            item.mimetype = 'application/vnd.apple.mpegurl'

    if not parser:
        return

    from .session import Session

    playlist_url = item.path.split('|')[0]

    try:
        resp = Session().get(playlist_url, headers=item.headers, cookies=item.cookies)
    except Exception as e:
        log.exception(e)
        result = False
    else:
        result = resp.ok

    if not result:
        gui.ok(_(_.QUALITY_PARSE_ERROR, error=_(_.QUALITY_HTTP_ERROR, code=resp.status_code)))
        return

    try:
        parser.parse(resp.text)
        qualities = parser.qualities()
        if not qualities:
            raise ParserError(_.QUALITY_NONE_FOUND)
    except Exception as e:
        log.exception(e)
        gui.ok(_(_.QUALITY_PARSE_ERROR, error=e))
        return

    if len(qualities) == 1:
        return

    if quality == QUALITY_ASK:
        quality = select_quality(qualities)
        if not quality:
            return False
        elif quality == QUALITY_SKIP:
            return

    min_bandwidth, max_bandwidth = parser.bandwidth_range(quality)
    set_settings(min_bandwidth, max_bandwidth, is_ia)
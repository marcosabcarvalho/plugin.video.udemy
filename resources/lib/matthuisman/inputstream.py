import os
import platform
import re
import shutil
import time

import xbmc, xbmcaddon

from . import gui, settings
from .log import log
from .constants import IA_ADDON_ID, IA_VERSION_KEY, IA_HLS_MIN_VER, IA_MPD_MIN_VER, IA_MODULES_URL, SESSION_CHUNKSIZE, IA_CHECK_EVERY
from .language import _
from .util import get_kodi_version, md5sum, remove_file
from .exceptions import InputStreamError

class InputstreamItem(object):
    manifest_type = ''
    license_type  = ''
    license_key   = ''
    mimetype      = ''
    checked       = None

    def do_check(self):
        return False

    def check(self):
        if self.checked is None:
            self.checked = self.do_check()
            
        return self.checked

class HLS(InputstreamItem):
    manifest_type = 'hls'
    mimetype      = 'application/vnd.apple.mpegurl'

    def do_check(self):
        return settings.getBool('use_ia_hls', False) and supports_hls()

class MPD(InputstreamItem):
    manifest_type = 'mpd'
    mimetype      = 'application/dash+xml'

    def do_check(self):
        return supports_mpd()

class Playready(InputstreamItem):
    manifest_type = 'ism'
    license_type  = 'com.microsoft.playready'
    mimetype      = 'application/vnd.ms-sstr+xml'

    def do_check(self):
        return supports_playready()

class Widevine(InputstreamItem):
    manifest_type = 'mpd'
    license_type  = 'com.widevine.alpha'
    mimetype      = 'application/dash+xml'

    def __init__(self, license_key=None, content_type='application/octet-stream', challenge='R{SSM}', response=''):
        self.license_key  = license_key
        self.content_type = content_type
        self.challenge    = challenge
        self.response     = response

    def do_check(self):
        return install_widevine()

def get_ia_addon(required=False, install=True):
    try:
        if install:
            xbmc.executebuiltin('InstallAddon({})'.format(IA_ADDON_ID), True)
            xbmc.executeJSONRPC('{{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{{"addonid":"{}","enabled":true}}}}'.format(IA_ADDON_ID))

        return xbmcaddon.Addon(IA_ADDON_ID)
    except:
        pass

    if required:
        raise InputStreamError(_.IA_NOT_FOUND)

    return None

def set_settings(settings):
    addon = get_ia_addon(install=False)
    if not addon:
        return

    log.debug('IA Set Settings: {}'.format(settings))

    for key in settings:
        addon.setSetting(key, str(settings[key]))

def get_settings(keys):
    addon = get_ia_addon(install=False)
    if not addon:
        return None

    settings = {}
    for key in keys:
        settings[key] = addon.getSetting(key)

    return settings

def open_settings():
    ia_addon = get_ia_addon(required=True)
    ia_addon.openSettings()

def supports_hls():
    ia_addon = get_ia_addon()
    return bool(ia_addon and int(ia_addon.getAddonInfo('version')[0]) >= IA_HLS_MIN_VER)

def supports_mpd():
    ia_addon = get_ia_addon()
    return bool(ia_addon and int(ia_addon.getAddonInfo('version')[0]) >= IA_MPD_MIN_VER)

def supports_playready():
    ia_addon = get_ia_addon()
    return bool(ia_addon and get_kodi_version() > 17 and xbmc.getCondVisibility('system.platform.android'))

def install_widevine(reinstall=False):
    ia_addon     = get_ia_addon(required=True)
    system, arch = _get_system_arch()
    kodi_version = get_kodi_version()

    if kodi_version < 18:
        raise InputStreamError(_(_.IA_KODI18_REQUIRED, system=system))

    elif system == 'Android':
        return True

    elif system == 'UWP':
        raise InputStreamError(_.IA_UWP_ERROR)

    elif 'aarch64' in arch or 'arm64' in arch:
        raise InputStreamError(_.IA_AARCH64_ERROR)

    last_check = int(ia_addon.getSetting('_last_check') or 0)
    ver_slug   = system + arch + str(kodi_version) + ia_addon.getAddonInfo('version')

    if ver_slug != ia_addon.getSetting(IA_VERSION_KEY):
        reinstall = True

    if not reinstall and time.time() - last_check < IA_CHECK_EVERY:
        return True

    ## DO INSTALL ##
    ia_addon.setSetting(IA_VERSION_KEY, '')
    ia_addon.setSetting('_last_check', str(int(time.time())))

    from .session import Session

    r = Session().get(IA_MODULES_URL)
    if r.status_code != 200:
        raise InputStreamError(_(_.ERROR_DOWNLOADING_FILE, filename=IA_MODULES_URL.split('/')[-1]))

    widevine    = r.json()['widevine']
    wv_platform = widevine['platforms'].get(system + arch, None)

    if not wv_platform:
        raise InputStreamError(_(_.IA_NOT_SUPPORTED, system=system, arch=arch, kodi_version=kodi_version))

    decryptpath = xbmc.translatePath(ia_addon.getSetting('DECRYPTERPATH')).decode("utf-8")
    url         = widevine['base_url'] + wv_platform['src']
    wv_path     = os.path.join(decryptpath, wv_platform['dst'])

    if not os.path.isdir(decryptpath):
        os.makedirs(decryptpath)

    if not _download(url, wv_path, wv_platform['md5']):
        return False

    ia_addon.setSetting(IA_VERSION_KEY, ver_slug)

    if reinstall:
        gui.ok(_.IA_WV_INSTALL_OK)

    return True

def _get_system_arch():
    if xbmc.getCondVisibility('system.platform.android'):
        system = 'Android'
    elif 'WindowsApps' in xbmc.translatePath('special://xbmcbin/'):
        system = 'UWP'
    else:
        system = platform.system()
    
    if system == 'Windows':
        arch = platform.architecture()[0]
    elif system == 'Android':
        arch = ''
    else:
        arch = platform.machine()

    if 'arm' in arch:
        if 'v6' in arch:
            arch = 'armv6'
        else:
            arch = 'armv7'

    elif arch == 'i686':
        arch = 'i386'

    return system, arch

def _download(url, dst_path, md5=None):
    filename   = url.split('/')[-1]
    downloaded = 0

    if os.path.exists(dst_path):
        if md5 and md5sum(dst_path) == md5:
            log.debug('MD5 of local file {} same. Skipping download'.format(filename))
            return True
        elif not gui.yes_no(_.NEW_IA_VERSION):
            return False
        else:
            remove_file(dst_path)
            
    from .session import Session

    with gui.progress(_(_.IA_DOWNLOADING_FILE, url=filename), heading=_.IA_WIDEVINE_DRM) as progress:
        resp = Session().get(url, stream=True)
        if resp.status_code != 200:
            raise InputStreamError(_(_.ERROR_DOWNLOADING_FILE, filename=filename))

        total_length = float(resp.headers.get('content-length', 1))

        with open(dst_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=SESSION_CHUNKSIZE):
                f.write(chunk)
                downloaded += len(chunk)
                percent = int(downloaded*100/total_length)

                if progress.iscanceled():
                    progress.close()
                    resp.close()

                progress.update(percent)

    if progress.iscanceled():
        remove_file(dst_path)            
        return False

    checksum = md5sum(dst_path)
    if checksum != md5:
        remove_file(dst_path)
        raise InputStreamError(_(_.MD5_MISMATCH, filename=filename, local_md5=checksum, remote_md5=md5))
    
    return True
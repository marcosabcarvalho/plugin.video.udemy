from .log import log
from .constants import ADDON

def format_string(string, _bold=False, _label=False, _color=None, _strip=False, **kwargs):
    if kwargs:
        string = string.format(**kwargs)

    if _strip:
        string = string.strip()

    if _label:
        _bold = True
        string = u'~ {} ~'.format(string)

    if _bold:
        string = u'[B]{}[/B]'.format(string)

    if _color:
        string = u'[COLOR {}]{}[/COLOR]'.format(_color, string)
        
    return string

def addon_string(id):
    string = ADDON.getLocalizedString(id)
    
    if not string:
        log.warning("LANGUAGE: Addon didn't return a string for id: {}".format(id))
        string = str(id)

    return string

class BaseLanguage(object):
    PLUGIN_LOGIN_REQUIRED       = 32000
    PLUGIN_NO_DEFAULT_ROUTE     = 32001
    PLUGIN_RESET_YES_NO         = 32002
    PLUGIN_RESET_OK             = 32003
    PLUGIN_CACHE_REMOVED        = 32004
    PLUGIN_CONTEXT_CLEAR_CACHE  = 32005
    ROUTER_NO_FUNCTION          = 32006
    ROUTER_NO_URL               = 32007
    IA_NOT_FOUND                = 32008
    IA_UWP_ERROR                = 32009
    IA_KODI18_REQUIRED          = 32010
    IA_AARCH64_ERROR            = 32011
    IA_NOT_SUPPORTED            = 32012
    NO_BRIGHTCOVE_SRC           = 32013
    IA_DOWNLOADING_FILE         = 32014
    IA_WIDEVINE_DRM             = 32015
    IA_ERROR_INSTALLING         = 32016
    USE_CACHE                   = 32017
    INPUTSTREAM_SETTINGS        = 32018
    CLEAR_DATA                  = 32019
    PLUGIN_ERROR                = 32020
    INSTALL_WV_DRM              = 32021
    IA_WV_INSTALL_OK            = 32022
    USE_IA_HLS                  = 32023
    LOGIN                       = 32024
    LOGOUT                      = 32025
    SETTINGS                    = 32026
    LOGOUT_YES_NO               = 32027
    LOGIN_ERROR                 = 32028
    SEARCH                      = 32029
    SEARCH_FOR                  = 32030
    NO_RESULTS                  = 32031
    PLUGIN_EXCEPTION            = 32032
    ERROR_DOWNLOADING_FILE      = 32033
    GENERAL                     = 32034
    PLAYBACK                    = 32035
    ADVANCED                    = 32036
    VERIFY_SSL                  = 32037
    SELECT_IA_VERSION           = 32038
    SERVICE_DELAY               = 32039
    MD5_MISMATCH                = 32040
    NO_ITEMS                    = 32041

    QUALITY_BEST                = 32043
    HTTP_TIMEOUT                = 32044
    HTTP_RETRIES                = 32045
    CHUNKSIZE                   = 32046
    WV_LATEST                   = 32047
    QUALITY_SKIP                = 32048
    NO_AUTOPLAY_FOUND           = 32049
    CONFIRM_MIGRATE             = 32050
    MIGRATE_OK                  = 32051
    NO_ERROR_MSG                = 32052

    QUALITY_CUSTOM              = 32054
    QUALITY_ASK                 = 32055

    PLAYBACK_ERROR              = 32057
    WV_INSTALLED                = 32058
    MAX_BANDWIDTH               = 32059
    QUALITY_LOWEST              = 32060
    PLAYBACK_QUALITY            = 32061

    PLAY_DEFAULT_ACTION         = 32063
    PLAY_FROM_START             = 32064
    PLAY_FROM_LIVE              = 32065
    PLAY_FROM_ASK               = 32066
    PLAY_FROM                   = 32067
    QUALITY_BITRATE             = 32068
    QUALITY_FPS                 = 32069
    SELECT_WV_VERSION           = 32070
    WV_UNKNOWN                  = 32071
    WV_NOT_LATEST               = 32072
    DISABLED                    = 32073

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if not isinstance(attr, int):
            return attr

        return addon_string(attr)

    def __call__(self, string, **kwargs):
        if isinstance(string, int):
            string = addon_string(string)

        return format_string(string, **kwargs)

_ = BaseLanguage()
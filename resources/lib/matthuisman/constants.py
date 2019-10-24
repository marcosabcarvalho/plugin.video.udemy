
import os

from kodi_six import xbmc, xbmcaddon

##### ADDON ####
ADDON          = xbmcaddon.Addon(os.environ.get('ADDON_ID', ''))
ADDON_ID       = ADDON.getAddonInfo('id')
ADDON_VERSION  = ADDON.getAddonInfo('version')
ADDON_NAME     = ADDON.getAddonInfo('name')
ADDON_PATH     = xbmc.translatePath(ADDON.getAddonInfo('path'))
ADDON_PROFILE  = xbmc.translatePath(ADDON.getAddonInfo('profile'))
ADDON_ICON     = ADDON.getAddonInfo('icon')
ADDON_FANART   = ADDON.getAddonInfo('fanart')
ADDON_DEV      = bool(int(os.environ.get('ADDON_DEV', '0')))
#################

#### DATABASE #####
DB_PATH         = os.path.join(ADDON_PROFILE, 'data.db')
DB_MAX_INSERTS  = 100
DB_PRAGMAS      = {
    'journal_mode': 'wal',
    'cache_size': -1 * 10000,  #10MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
}
DB_TABLENAME = '_db'
###################

##### USERDATA ####
USERDATA_KEY = '_userdata'
###############

##### CACHE #####
CACHE_TABLENAME      = '_cache'
CACHE_CHECKSUM       = ADDON_VERSION # Recreates cache when new addon version
CACHE_EXPIRY         = (60*60*24) # 24 Hours
CACHE_CLEAN_INTERVAL = (60*60*4)  # 4 Hours
CACHE_CLEAN_KEY      = '_cache_cleaned'
#################

#### ROUTING ####
ROUTE_TAG              = '_'
ROUTE_RESET            = '_reset'
ROUTE_SETTINGS         = '_settings'
ROUTE_IA_SETTINGS      = '_ia_settings'
ROUTE_IA_INSTALL       = '_ia_install'
ROUTE_CLEAR_CACHE      = '_clear_cache'
ROUTE_SERVICE          = '_service'
ROUTE_SERVICE_INTERVAL = (60*5)
ROUTE_LIVE_TAG         = '_l'
ROUTE_LIVE_SUFFIX      = '.pvr'
ROUTE_URL_TAG          = '_url'
FORCE_RUN_FLAG         = '_force_run'
ROUTE_AUTOPLAY_TAG     = '_autoplay'
#################

#### INPUTSTREAM ADAPTIVE #####
IA_ADDON_ID     = 'inputstream.adaptive'
IA_VERSION_KEY  = '_version'
IA_HLS_MIN_VER  = 2
IA_MPD_MIN_VER  = 2
IA_MODULES_URL  = 'https://k.mjh.nz/.decryptmodules/modules.v3.json'
IA_CHECK_EVERY  = 86400 #24 hours
###################

#### MISC #####
NOARG = object()
#################

#### LOG #####
LOG_ID     = ADDON_ID
LOG_FORMAT = u'%(name)s - %(message)s'
#################

#### GUI ####
GUI_DEFAULT_AUTOCLOSE = 120000 #2mins

## QUALITY ##
QUALITY_ASK      = -1
QUALITY_BEST     = -2
QUALITY_LOWEST   = -3
QUALITY_SKIP     = -4
QUALITY_CUSTOM   = -5
QUALITY_DISABLED = -6
QUALITY_TYPES    = [QUALITY_ASK, QUALITY_BEST, QUALITY_LOWEST, QUALITY_SKIP, QUALITY_CUSTOM, QUALITY_DISABLED]
QUALITY_TAG      = '_quality'

## PLAY FROM ##
PLAY_FROM_ASK    = 0
PLAY_FROM_LIVE   = 1
PLAY_FROM_START  = 2
PLAY_FROM_TYPES  = [PLAY_FROM_ASK, PLAY_FROM_LIVE, PLAY_FROM_START]
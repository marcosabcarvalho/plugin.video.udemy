from matthuisman.language import BaseLanguage

class Language(BaseLanguage):
    LOGIN            = 30000
    MY_COURSES       = 30001
    LOGOUT           = 30002
    SETTINGS         = 30003
    ASK_USERNAME     = 30004
    ASK_PASSWORD     = 30005
    LOGIN_ERROR      = 30006
    LOGOUT_YES_NO    = 30007
    COURSE_INFO      = 30008
    SECTION_LABEL    = 30009
    NO_STREAM_ERROR  = 30010
    NO_COURSES       = 30011

_ = Language()
import gettext as native_gettext

from tasklocal import local


_translations = {}
_local = local()
default_language = 'en-uk'
ACTIVE_LANG_FIELD = 'language'


def activate(language):
    setattr(_local, ACTIVE_LANG_FIELD, language)


def get_translation(language_code: str):
    if language_code not in _translations:
        _translations[language_code] = native_gettext.translation(
            None, localedir='locale', languages=[language_code]
        )

    return _translations[language_code]


def gettext(text):
    translation = get_translation(getattr(_local, ACTIVE_LANG_FIELD, default_language))
    return translation.gettext(text)

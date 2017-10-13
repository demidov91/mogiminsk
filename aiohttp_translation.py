import gettext as native_gettext
import os

from tasklocal import local


_translations = {}
_local = local()
default_language = 'en-uk'
ACTIVE_LANG_FIELD = 'language'
BASE_DIR = os.path.dirname(__file__)


def activate(language):
    setattr(_local, ACTIVE_LANG_FIELD, language)


def get_translation(language_code: str):
    if language_code not in _translations:
        _translations[language_code] = native_gettext.translation(
            'messages', localedir=os.path.join(BASE_DIR, 'locale'), languages=[language_code]
        )

    return _translations[language_code]


def gettext(text):
    translation = get_translation(getattr(_local, ACTIVE_LANG_FIELD, default_language))
    return translation.gettext(text)

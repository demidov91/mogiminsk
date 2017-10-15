import logging

TELEGRAM_TOKEN = ''
DB_CONNECTION = {}
LOGENTRIES_TOKEN = ''
LANGUAGE = 'ru'

try:
    from mogiminsk.local_settings import *
except ImportError:
    pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(processName)s] [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'logentries': {
            'level': 'DEBUG',
            'class': 'logentries.LogentriesHandler',
            'token': LOGENTRIES_TOKEN,
            'format': logging.Formatter(
                '%(asctime)s : %(processName)s %(levelname)s, %(message)s',
                '%a %b %d %H:%M:%S %Z %Y'
            ),
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logentries'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

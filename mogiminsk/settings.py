TELEGRAM_TOKEN = ''
DB_CONNECTION = {}
LOGENTRIES_TOKEN = ''

try:
    from mogiminsk.local_settings import *
except ImportError:
    pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'logentries': {
            'level': 'DEBUG',
            'class': 'logentries.LogentriesHandler',
            'token': LOGENTRIES_TOKEN,
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

import logging.config

TELEGRAM_TOKEN = ''
VIBER_TOKEN = ''
DB_CONNECTION = {}
LOGENTRIES_TOKEN = ''
LANGUAGE = 'ru'

EMAIL_FEEDBACK_SUBJECT = 'Mogiminsk feedback'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_FROM = 'dmitryDemidov91@gmail.com'
EMAIL_TO = 'demidov91@mail.ru',

TG_CONTACT = '@dzimdziam'
VIBER_CONTACT = 'demidov91@mail.ru'

try:
    from mogiminsk.local_settings import *
except ImportError:
    pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [p%(process)d] [%(levelname)s] %(name)s: %(message)s'
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
                '%(asctime)s : [p%(process)d] %(levelname)s, %(message)s',
                '%a %b %d %H:%M:%S %Z %Y'
            ),
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
            'formatter': 'standard',
            'environment': SENTRY_ENVIRONMENT,
            'enable_breadcrumbs': False,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logentries'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

logging.config.dictConfig(LOGGING)

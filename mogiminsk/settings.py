import os
import logging.config

BASE_DIR = os.path.dirname(os.getcwd())
TELEGRAM_TOKEN = ''
VIBER_TOKEN = ''
DB_CONNECTION = {}
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
        'filesystem': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,       # 10 Mb
            'backupCount': 10,                  # 10 * 10Mb == 100Mb
            'filename': os.path.join(BASE_DIR, 'logs', 'mogiminsk.log'),
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
            'handlers': ['filesystem', 'sentry'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

logging.config.dictConfig(LOGGING)

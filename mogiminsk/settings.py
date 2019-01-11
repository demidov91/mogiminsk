import os
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
VIBER_TOKEN = os.environ.get('VIBER_TOKEN', '')
TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY', '')
VIBER_API_KEY = os.environ.get('VIBER_API_KEY', '')

DB_CONNECTION = {
    'drivername': 'postgres',
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'database': os.environ['DB_DATABASE'],
    'username': os.environ['DB_USERNAME'],
    'password':  os.environ['DB_PASSWORD'],
}
LANGUAGE = 'ru'

EMAIL_FEEDBACK_SUBJECT = 'Mogiminsk feedback'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_FROM = 'dmitryDemidov91@gmail.com'
EMAIL_TO = 'demidov91@mail.ru',

TG_CONTACT = '@dzimdziam'
VIBER_CONTACT = 'demidov91@mail.ru'

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
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': os.environ['SENTRY_DSN'],
            'formatter': 'standard',
            'environment': os.environ['SENTRY_ENVIRONMENT'],
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

import os
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
VIBER_TOKEN = os.environ.get('VIBER_TOKEN')

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
VIBER_API_KEY = os.environ.get('VIBER_API_KEY')


DB_CONNECTION = {
    'drivername': 'postgres',
    'host': 'postgres',
    'port': '5432',
    'database': 'postgres',
    'username': 'postgres',
    'password':  os.environ['POSTGRES_PASSWORD'],
}
LANGUAGE = 'ru'


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
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': os.environ.get('SENTRY_DSN'),
            'formatter': 'standard',
            'environment': os.environ.get('SENTRY_ENVIRONMENT'),
            'enable_breadcrumbs': False,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

logging.config.dictConfig(LOGGING)

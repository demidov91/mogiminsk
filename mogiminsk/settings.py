import os
import logging.config

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
VIBER_TOKEN = os.environ['VIBER_TOKEN']
TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']
VIBER_API_KEY = os.environ['VIBER_API_KEY']


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
    },
    'loggers': {
        '': {
            'handlers': ['filesystem'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    environment=os.environ['SENTRY_ENVIRONMENT'],
    integrations=[
        LoggingIntegration(
            level=logging.DEBUG,
            event_level=logging.WARNING
        ),
    ],
)
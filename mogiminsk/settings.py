import os
import logging.config

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


logger = logging.getLogger(__name__)


def get_env(key: str) -> str:
    if key not in os.environ:
        logger.warning('%s is not set in environment', key)
        return None
    return os.environ[key]


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TELEGRAM_TOKEN = get_env('TELEGRAM_TOKEN')
VIBER_TOKEN = get_env('VIBER_TOKEN')
TELEGRAM_API_KEY = get_env('TELEGRAM_API_KEY')
VIBER_API_KEY = get_env('VIBER_API_KEY')


DB_CONNECTION = {
    'drivername': 'postgres',
    'host': get_env('DB_HOST'),
    'port': get_env('DB_PORT'),
    'database': get_env('DB_DATABASE'),
    'username': get_env('DB_USERNAME'),
    'password':  get_env('DB_PASSWORD'),
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
    dsn=get_env('SENTRY_DSN'),
    environment=get_env('SENTRY_ENVIRONMENT'),
    integrations=[
        LoggingIntegration(
            level=logging.DEBUG,
            event_level=logging.WARNING
        ),
    ],
)
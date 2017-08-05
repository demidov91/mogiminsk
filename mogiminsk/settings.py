TELEGRAM_TOKEN = None
DB_CONNECTION = None

try:
    from mogiminsk.local_settings import *
except ImportError:
    pass

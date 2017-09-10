from mogiminsk.utils import get_db
from mogiminsk.models import Trip


def _get_current_trip(context, db=None):
    db = db or get_db()
    return db.query(Trip).get(context['trip'])


def get_sms_code(context):
    trip = _get_current_trip(context)
    return context.get(f'sms_{trip.car.provider.identifier}')


def set_sms_code(context, code):
    trip = _get_current_trip(context)
    context[f'sms_{trip.car.provider.identifier}'] = code
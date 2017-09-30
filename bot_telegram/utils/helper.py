"""
Helper module to use FROM state classes.
"""

from mogiminsk.utils import get_db
from mogiminsk.models import Trip, Station, Purchase
from mogiminsk_interaction.utils import get_connector
from mogiminsk_interaction.connectors.core import BaseConnector


def _get_current_trip(context, db=None):
    db = db or get_db()
    return db.query(Trip).get(context['trip'])


def _get_sms_key(trip: Trip) -> str:
    return f'sms_{trip.car.provider.identifier}'


def get_sms_code(context):
    trip = _get_current_trip(context)
    return context.get(_get_sms_key(trip))


def set_sms_code(context, code):
    trip = _get_current_trip(context)
    context[_get_sms_key(trip)] = code


async def purchase(user, context: dict, sms_code: str=None) ->BaseConnector:
    db = get_db()

    trip = db.query(Trip).get(context['show'])
    station = db.query(Station).get(context['station'])

    connector = get_connector(trip.car.provider.identifier)

    await connector.purchase(
        start_datetime=trip.start_datetime,
        direction=context['where'],
        seat=int(context['seat']),
        first_name=user.first_name,
        station=station.identifier,
        notes=context.get('notes'),
        phone=user.phone,
        sms_code=sms_code,
    )

    return connector


async def cancel_purchase(user, context, sms_code=None) ->BaseConnector:
    db = get_db()
    purchase = db.query(Purchase).get(context['cancel'])

    connector = get_connector(purchase.trip.car.provider.identifier)

    remote_purchases = connector.get_purchases(user)
    remote_purchase = connector.choose_purchase(remote_purchases, purchase.trip.start_datetime, purchase.trip.car)
    connector.cancel_remote_purchase(remote_purchase)

    return connector


async def store_purchase_event(user, context):
    trip_id = int(context['show'])
    seat = int(context['seat'])
    station_id = int(context['station'])
    notes = context.get('notes')

    purchase = Purchase(
        trip_id=trip_id,
        seats=seat,
        station_id=station_id,
        notes=notes,
        user=user
    )

    get_db().add(purchase)

"""
Helper module to use FROM state classes.
"""

from mogiminsk.utils import get_db
from mogiminsk.models import Trip, Station, Purchase
from mogiminsk_interaction.utils import get_connector
from mogiminsk_interaction.connectors.core import BaseConnector


class SmsStorage:
    def __init__(self, context):
        self.context = context

    def _get_sms_key(trip: Trip=None, car=None, provider=None, provider_identifier=None) -> str:
        if provider_identifier:
            identifier = provider_identifier

        elif provider:
            identifier = provider.identifier

        elif car:
            identifier = car.provider.identifier

        elif trip:
            identifier = trip.car.provider.identifier

        else:
            raise ValueError()

        return f'sms_{identifier}'

    def get_sms_code(self, trip):
        return self.context.get(self._get_sms_key(trip=trip))

    def set_sms_code(self, code, trip=None, car=None, provider=None, provider_identifier=None):
        self.context[self._get_sms_key(
            trip=trip, car=car, provider=provider, provider_identifier=provider_identifier
        )] = code


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
    trip = db.query(Purchase).get(context['purchase_cancel']).trip

    sms_storage = SmsStorage(context)

    if sms_code:
        sms_storage.set_sms_code(sms_code, trip=trip)

    else:
        sms_code = sms_storage.get_sms_code(trip=trip)

    connector = get_connector(trip.car.provider.identifier)
    connector.sms_code = sms_code
    connector.cancel_purchase(
        user.phone, trip.start_datetime, trip.direction, trip.car.name
    )

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

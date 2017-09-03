from sqlalchemy import and_

from mogiminsk.utils import get_db
from mogiminsk.models import Purchase, Trip, Car, Provider


def purchase_state_or_other(user, data):
    if not user.phone:
        return 'phone'

    if not user.first_name:
        return 'firstname'

    if 'station' not in data:
        _initialize_station(user, data)
        if 'station' not in data:
            return 'station'

    if 'seat' not in data:
        _initialize_seat(user, data)
        if 'seat' not in data:
            return 'seat'

    return 'purchase'


def _initialize_station(user, data):
    db = get_db()
    trip = db.query(Trip).get(data['show'])

    last_purchase = db.query(Purchase, Trip, Car, Provider).filter(and_(
        Trip.direction == trip.direction,
        Purchase.user_id == user.id,
        Provider.id == trip.car.provider_id,
    )).first()
    if last_purchase is None:
        return

    data['station'] = last_purchase.station_id
    data['station_name'] = last_purchase.station_name


def _initialize_seat(user, data):
    db = get_db()

    last_purchase = db.query(Purchase).filter(
        Purchase.user_id == user.id
    ).order_by(Purchase.created_at.desc()).first()

    if last_purchase is None:
        return

    data['seat'] = last_purchase.seats

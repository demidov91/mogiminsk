from mogiminsk.utils import get_db
from mogiminsk.models import Purchase, Trip


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
    last_purchase = db.query(Purchase, )
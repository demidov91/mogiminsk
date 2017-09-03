import logging

from sqlalchemy import and_

from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other
from .base import BaseState
from mogiminsk.utils import get_db
from mogiminsk.models import Station, Trip, Provider


logger = logging.getLogger(__name__)


class StationState(BaseState):
    def get_intro_message(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['trip'])
        stations = tuple(get_db().query(Station, Provider).filter(
            and_(
                Provider.id == trip.car.provider_id,
                Station.direction == trip.direction,
                not Station.is_removed
            )
        ))

        if len(stations) == 0:
            raise ValueError(f'There are no stations available in db for '
                             f'provider {trip.car.provider.identifier}'
                             f'and direction {trip.direction}')

        buttons = [
            [{'text': x.name, 'data': x.id}] for x in stations
        ]

        return BotMessage('Choose start station:', buttons=buttons)

    def process(self):
        try:
            station_id = int(self.value)
            station = get_db().query(Station).get(station_id)
            self.data['station_name'] = station.name
        except:
            logger.exception("Couldn't get pickup station.")
            self.message_was_not_recognized = True
            return

        self.set_state(purchase_state_or_other(self.user))


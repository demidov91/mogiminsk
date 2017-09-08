import logging

from sqlalchemy import and_

from bot_telegram.messages import BotMessage
from .base import BaseState
from mogiminsk.utils import get_db
from mogiminsk.models import Station, Trip, Provider


logger = logging.getLogger(__name__)


class StationState(BaseState):
    def get_intro_message(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['show'])
        stations = tuple(get_db().query(Station).join(Provider).filter(
            and_(
                Provider.id == trip.car.provider_id,
                Station.direction == trip.direction,
                Station.is_removed == False
            )
        ))

        if len(stations) == 0:
            raise ValueError(f'There are no stations available in db for '
                             f'provider {trip.car.provider.identifier}'
                             f'and direction {trip.direction}')

        buttons = [
            [{'text': x.name, 'data': str(x.id)}] for x in stations
        ]
        buttons.append([{'text': 'Back', 'data': 'back'}])

        return BotMessage('Choose start station:', buttons=buttons)

    async def process(self):
        try:
            station_id = int(self.value)
            station = get_db().query(Station).get(station_id)
            self.data['station_name'] = station.name
        except:
            logger.exception("Couldn't get pickup station.")
            self.message_was_not_recognized = True
            return

        self.set_state('purchase')


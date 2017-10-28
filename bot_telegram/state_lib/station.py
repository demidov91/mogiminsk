import logging

from aiohttp_translation import gettext_lazy as _

from bot.messages.base import BotMessage, BACK
from .base import BaseState
from mogiminsk.services.trip import TripService
from mogiminsk.services.station import StationService


logger = logging.getLogger(__name__)


class StationState(BaseState):
    def get_intro_message(self):
        trip_service = TripService.get_service(self.data['show'])

        stations = trip_service.get_stations()

        if stations.count() == 0:
            raise ValueError(f'There are no stations available in db for '
                             f'provider {trip_service.provider_name()}'
                             f'and direction {trip_service.direction_name()}')

        buttons = [
            [{'text': x.name, 'data': str(x.id)}] for x in stations
        ]
        buttons.append([BACK])

        return BotMessage(_('Choose start station:'), buttons=buttons)

    async def get_back_state(self):
        if self.data.get('station'):
            return 'purchase'

        return 'show'

    async def process(self):
        try:
            station_id = int(self.value)
            station = StationService.get(station_id)
            self.data['station_name'] = station.name
        except:
            logger.exception("Couldn't get pickup station.")
            self.message_was_not_recognized = True
            return

        self.set_state('purchase')


import logging

from aiohttp_translation import gettext_lazy as _

from bot.messages.base import BotMessage, BACK
from .base import BaseState
from mogiminsk.defines import VIBER_ROWS_LIMIT
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

        viber_limit_with_back = VIBER_ROWS_LIMIT - 1
        viber_limit_with_back_and_navigate = viber_limit_with_back - 1

        if len(buttons) > viber_limit_with_back:
            if self.data.get('station__last'):
                buttons = buttons[viber_limit_with_back_and_navigate:]
                buttons.insert(0, [{
                    'text': _('...previous'),
                    'data': 'first',
                }])

            else:
                buttons = buttons[:viber_limit_with_back_and_navigate]
                buttons.append([{
                    'text': _('more...'),
                    'data': 'last',
                }])

        buttons.append([BACK])
        return BotMessage(_('Choose start station:'), buttons=buttons)

    async def get_back_state(self):
        if self.data.get('station') is not None and self.data['station'].isdigit():
            return 'purchase'

        return 'show'

    async def process(self):
        if self.value == 'first':
            self.data['station__last'] = False
            return

        if self.value == 'last':
            self.data['station__last'] = True
            return

        try:
            station_id = int(self.value)
            station = StationService.get(station_id)
            self.data['station_name'] = station.name
        except:
            logger.exception("Couldn't get pickup station.")
            self.message_was_not_recognized = True
            return

        self.data['station__last'] = False
        self.set_state('purchase')

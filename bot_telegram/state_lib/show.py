from aiohttp_translation import gettext_lazy as _
import re
from typing import Iterable, Dict, Collection

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.defines import FULL_TRIPS_SWITCH
from mogiminsk.models import Trip
from mogiminsk.services.trip import TripService
from mogiminsk_interaction.utils import has_connector


def trip_to_line(trip: Trip) -> Collection[Dict]:
    trip_service = TripService(trip)

    if trip.remaining_seats:
        description = '{}, {} ({})'.format(
            trip_service.instance.start_datetime.strftime('%H:%M'),
            trip_service.provider_name(),
            trip_service.instance.remaining_seats
        )

    else:
        description = '{}, {}'.format(
            trip_service.instance.start_datetime.strftime('%H:%M'),
            trip_service.provider_name()
        )

    is_bookable = has_connector(trip_service.provider().identifier)
    action = f'purchase_{trip_service.id}' if is_bookable else f'trip_{trip_service.id}'
    action_text = b'\xF0\x9F\x9A\x90'.decode('utf-8') \
        if is_bookable else b'\xF0\x9F\x93\x9E'.decode('utf-8')

    return [{
        'text': f'{action_text} {description}',
        'data': action,
    }]


class ShowState(BaseState):
    action_template = re.compile('(?P<action>(trip|purchase))_(?P<id>\d+)')
    back = 'time'

    def get_intro_message(self):
        trip_id_list = self.data['trip_id_list']
        show_shorten = (len(trip_id_list) > 4) and not self.data.get(FULL_TRIPS_SWITCH)

        if show_shorten:
            trip_id_list = trip_id_list[:3]

        trips = TripService.id_list(trip_id_list).order_by(Trip.start_datetime)
        buttons = [
            trip_to_line(trip) for trip in trips
        ]

        if show_shorten:
            buttons.append([{
                'text': _('More'),
                'data': 'full',
            }])

        buttons.append([{
            'text': _('Back'),
            'data': 'back',
        }])
        return BotMessage(text=_('Choose trip:'), buttons=buttons)

    async def process(self):
        if self.value == 'full':
            self.data[FULL_TRIPS_SWITCH] = True
            return
        match = self.action_template.match(self.value)
        if not match:
            self.message_was_not_recognized = True
            return

        self.data[self.get_name()] = match.group('id')
        next_state = match.group('action')

        if next_state == 'purchase':
            self.set_state('purchase')

        else:
            self.set_state(next_state)

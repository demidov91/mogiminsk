import re
from typing import Dict, Collection

from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from bot.state_lib.base import BaseState
from bot_telegram.defines import FULL_TRIPS_SWITCH
from mogiminsk.models import Trip
from mogiminsk.services.trip import TripService
from mogiminsk_interaction.utils import has_connector


def _build_trip_description_part_1(ts: TripService):
    if not ts.instance.is_default_price():
        provider_name = ts.provider_short_name()
    else:
        provider_name = ts.provider_name()

    return '{}, {}'.format(
        ts.instance.start_datetime.strftime('%H:%M'),
        provider_name
    )


def _build_trip_description_part_2(ts: TripService):
    if not ts.instance.is_default_price():
        return _('%dr.') % ts.instance.cost

    return ''


def _build_trip_description_part_3(ts: TripService):
    if ts.instance.remaining_seats:
        if not ts.instance.is_default_price():
            return _('({} seats)').format(ts.instance.remaining_seats)

        return '({})'.format(ts.instance.remaining_seats)

    return ''


def trip_to_line(trip: Trip) -> Collection[Dict]:
    trip_service = TripService(trip)

    parts = [
        _build_trip_description_part_1(trip_service),
        _build_trip_description_part_2(trip_service),
        _build_trip_description_part_3(trip_service),
    ]
    description = ' '.join([x for x in parts if x])

    is_bookable = has_connector(trip_service.provider().identifier)
    action = f'purchase_{trip_service.id}' if is_bookable else f'trip_{trip_service.id}'
    icon = '\U0001f690' if is_bookable else '\U0001f4de'

    return [{
        'text': f'{icon} {description}',
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

        buttons.append([BACK])
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
        self.set_state(match.group('action'))

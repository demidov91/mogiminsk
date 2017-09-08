import re
from typing import Iterable, Dict, Collection

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.defines import FULL_TRIPS_SWITCH
from mogiminsk.models import Trip
from mogiminsk.utils import get_db
from mogiminsk_interaction.utils import has_connector


def get_trips(trip_id_list: Iterable[int]) -> Iterable[Trip]:
    return get_db().query(Trip).filter(Trip.id.in_(trip_id_list))


def trip_to_line(trip: Trip) -> Collection[Dict]:
    if trip.remaining_seats:
        description = '{}, {} ({})'.format(
            trip.start_datetime.strftime('%H:%M'),
            trip.car.provider.name,
            trip.remaining_seats
        )

    else:
        description = '{}, {}'.format(
            trip.start_datetime.strftime('%H:%M'), trip.car.provider.name
        )

    is_bookable = has_connector(trip.car.provider.identifier)
    action = f'purchase_{trip.id}' if is_bookable else f'trip_{trip.id}'
    action_text = b'\xF0\x9F\x9A\x90'.decode('utf-8') \
        if is_bookable else b'\xF0\x9F\x93\x9E'.decode('utf-8')

    return [{
        'text': f'{action_text} {description}',
        'data': action,
    }]


class ShowState(BaseState):
    action_template = re.compile('(?P<action>(trip|purchase))_(?P<id>\d+)')

    def get_intro_message(self):
        trip_id_list = self.data['trip_id_list']
        show_shorten = (len(trip_id_list) > 4) and not self.data.get(FULL_TRIPS_SWITCH)

        if show_shorten:
            trip_id_list = trip_id_list[:3]

        trips = get_trips(trip_id_list)
        buttons = [
            trip_to_line(trip) for trip in trips
        ]

        if show_shorten:
            buttons.append([{
                'text': 'More',
                'data': 'full',
            }])

        buttons.append([{
            'text': 'Back',
            'data': 'back',
        }])
        return BotMessage(text='Choose trip:', buttons=buttons)

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

from typing import Iterable

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.defines import FULL_TRIPS_SWITCH
from mogiminsk.models import Trip
from mogiminsk.utils import get_db


def get_trips(trip_id_list: Iterable[int]) -> Iterable[Trip]:
    return get_db().query(Trip).filter(Trip.id.in_(trip_id_list))


def trip_to_button(trip: Trip) -> dict:
    return {
        'text': '{}, {}'.format(
            trip.start_datetime.strftime('%H:%M'), trip.car.provider.name
        ),
        'data': str(trip.id),
    }


class ShowState(BaseState):
    @classmethod
    def get_intro_message(cls, data):
        trip_id_list = data['trip_id_list']
        show_shorten = (len(trip_id_list) > 4) and not data.get(FULL_TRIPS_SWITCH)

        if show_shorten:
            trip_id_list = trip_id_list[:3]

        trips = get_trips(trip_id_list)
        buttons = [
            [trip_to_button(trip)] for trip in trips
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

    def process(self):
        if self.value == 'full':
            self.data[FULL_TRIPS_SWITCH] = True
            return

        self.set_state('trip')

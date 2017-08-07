from typing import Iterable

from bot_telegram.states import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.defines import FIRST_TRIPS_SWITCH
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
        show_first = data.get(FIRST_TRIPS_SWITCH)

        if show_first:
            trip_id_list = trip_id_list[:3]

        trips = get_trips(trip_id_list)
        buttons = [
            [trip_to_button(trip)] for trip in trips
        ]

        if show_first:
            buttons.append([{
                'text': 'More',
                'data': 'full',
            }])

        buttons.append([{
            'text': 'Back',
            'data': 'back',
        }])
        return BotMessage(text='Choose trip:', buttons=buttons)

    def consume(self, text: str):
        if self.value == 'back':
            del self.data[FIRST_TRIPS_SWITCH]
            self.set_state('time')
            return

        if self.value == 'full':
            self.data[FIRST_TRIPS_SWITCH] = False
            return

        self.set_state('trip')

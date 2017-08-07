from typing import Iterable

from bot_telegram.states import BaseState
from bot_telegram.messages import BotMessage
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


class ShowFullState(BaseState):
    @classmethod
    def get_intro_message(cls, data):
        trip_id_list = data['trip_id_list']
        trips = get_trips(trip_id_list)
        buttons = [
            [trip_to_button(trip)] for trip in trips
        ]
        buttons.append([{
            'text': 'Back',
            'data': 'back',
        }])
        return BotMessage(text='Choose trip:', buttons=buttons)

    def consume(self, text: str):
        if self.value == 'back':
            self.set_state('time')
            return

        self.set_state('tripafterfull')


class ShowSplitState(BaseState):
    @classmethod
    def get_intro_message(cls, data):
        trip_id_list = data['trip_id_list']
        trips = get_trips(trip_id_list[:4])
        buttons = [
            [trip_to_button(trip)] for trip in trips
        ]
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
            self.set_state('time')
            return

        if self.value == 'full':
            self.set_state('showfull')
            return

        self.set_state('tripaftersplit')

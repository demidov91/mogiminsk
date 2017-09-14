import datetime
import re

from sqlalchemy import or_

from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.base import BaseState
from mogiminsk.models import Trip
from mogiminsk.defines import DATE_FORMAT, DATE_TIME_FORMAT
from mogiminsk.utils import get_db


class TimeState(BaseState):
    back = 'date'

    _intro_message = BotMessage(
        text='Enter time. For example: 7, 1125 or 16:40.',
        buttons=[
            [{'data': 'back', 'text': 'Back'}]
        ],
    )

    time_pattern = re.compile('(?P<hours>\d{1,2}?):?(?P<minutes>\d{2})?\s*$')
    is_callback_state = False

    async def process(self):
        match = self.time_pattern.search(self.text)
        if match is None:
            self.message_was_not_recognized = True
            return

        hours = match.group('hours')
        minutes = match.group('minutes') or '00'

        cleared_time = f'{hours}:{minutes}'

        try:
            datetime.datetime.strptime(cleared_time, '%H:%M')
        except ValueError:
            self.message_was_not_recognized = True
            return

        self.data[self.get_name()] = cleared_time
        self.data['trip_id_list'] = self.get_trip_id_list()

        if len(self.data['trip_id_list']) == 0:
            self.set_state('where')
            self.add_message('No trips found :(')
            return

        self.set_state('show')

    def get_trip_id_list(self):
        start_datetime_string = '{} {}'.format(self.data['date'], self.data['time'])
        start_datetime = datetime.datetime.strptime(start_datetime_string, DATE_TIME_FORMAT)

        return TripFetcher(start_datetime, self.data['where']).produce()


class TripFetcher:
    success = True

    big_start_datetime_range = datetime.timedelta(hours=1), datetime.timedelta(hours=1)
    small_start_datetime_range = datetime.timedelta(minutes=15), datetime.timedelta(minutes=30)

    def __init__(self, dt: datetime.datetime, direction: str):
        super().__init__()
        self.dt = dt
        self.direction = direction

    def produce(self):
        big_time_range = self.dt - self.big_start_datetime_range[0],\
                         self.dt + self.big_start_datetime_range[1]
        small_time_range = self.dt - self.small_start_datetime_range[0],\
                           self.dt + self.small_start_datetime_range[1]

        # Really we need only id list here.
        trips_long_list = tuple(
            get_db().query(Trip).filter(
                Trip.direction == self.direction).filter(
                    Trip.start_datetime.between(*big_time_range)).filter(
                        or_(
                            Trip.remaining_seats > 0, Trip.remaining_seats.is_(None)
                        )).filter(
                            Trip.is_removed.is_(False)
            )
        )

        trips_short_list = tuple(filter(
            lambda x: small_time_range[0] <= x.start_datetime <= small_time_range[1],
            trips_long_list
        ))

        if len(trips_short_list) < 2:
            trips = trips_long_list

        else:
            trips = trips_short_list

        if len(trips) == 0:
            return self.no_trips()

        trips = sorted(trips, key=lambda x: x.start_datetime)

        return tuple(x.id for x in trips)

    def no_trips(self):
        return ExtendedTripFetcher(self.dt, self.direction).produce()


class ExtendedTripFetcher(TripFetcher):
    big_start_datetime_range = datetime.timedelta(hours=6), datetime.timedelta(hours=8)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(hours=4)

    def no_trips(self):
        return ()

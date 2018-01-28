import datetime

from sqlalchemy import or_

from aiohttp_translation import gettext_lazy as _
from bot.messages.time import MorningMessage, DayMessage, EveningMessage
from bot.state_lib.base import BaseState
from mogiminsk.defines import DATE_TIME_FORMAT
from mogiminsk.models import Trip
from mogiminsk.utils import get_db


class TimeState(BaseState):
    back = 'timeperiod'

    def get_intro_message(self):
        if self.data['timeperiod'] == 'morning':
            return MorningMessage()

        if self.data['timeperiod'] == 'day':
            return DayMessage()

        if self.data['timeperiod'] == 'evening':
            return EveningMessage()

        raise ValueError(self.data['timeperiod'])

    async def process(self):
        is_morning = False
        is_evening = False

        if self.value == MorningMessage.FIRST:
            is_morning = True
            time = MorningMessage.FIRST_TIME

        elif self.value == EveningMessage.LAST:
            is_evening = True
            time = EveningMessage.LAST_TIME

        else:
            time = self.value

        self.data['trip_id_list'] = self.get_trip_id_list(time, is_morning, is_evening)

        if len(self.data['trip_id_list']) == 0:
            self.set_state('where')
            self.add_message(_('No trips found :('))
            return

        self.set_state('show')

    def get_trip_id_list(self, time_string, is_morning, is_evening):
        start_datetime_string = '{} {}'.format(self.data['date'], time_string)
        start_datetime = datetime.datetime.strptime(start_datetime_string, DATE_TIME_FORMAT)

        if is_morning:
            fetcher = MorningTripFetcher(start_datetime, self.data['where'])

        elif is_evening:
            fetcher = EveningTripFetcher(start_datetime, self.data['where'])

        else:
            fetcher = TripFetcher(start_datetime, self.data['where'])

        return fetcher.produce()


class TripFetcher:
    success = True

    big_start_datetime_range = datetime.timedelta(hours=1), datetime.timedelta(hours=1)
    small_start_datetime_range = datetime.timedelta(minutes=15), datetime.timedelta(minutes=30)

    def __init__(self, dt: datetime.datetime, direction: str):
        self.dt = dt
        self.direction = direction

    def produce(self):
        current_time = datetime.datetime.now()

        big_time_range = [
            max(self.dt - self.big_start_datetime_range[0], current_time),
            max(self.dt + self.big_start_datetime_range[1], current_time)
        ]
        small_time_range = [
            max(self.dt - self.small_start_datetime_range[0], current_time),
            max(self.dt + self.small_start_datetime_range[1], current_time)
        ]

        if big_time_range[1] == current_time:
            return self.no_trips()

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


class MorningTripFetcher(TripFetcher):
    """
    Returns first trips of the day.
    """
    big_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(minutes=-1)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(minutes=-1)


class EveningTripFetcher(TripFetcher):
    """
    Returns last trips of the day.
    """
    big_start_datetime_range = datetime.timedelta(hours=0), datetime.timedelta(hours=3)
    small_start_datetime_range = datetime.timedelta(hours=0), datetime.timedelta(hours=3)


class ExtendedTripFetcher(TripFetcher):
    big_start_datetime_range = datetime.timedelta(hours=6), datetime.timedelta(hours=8)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(hours=4)

    def no_trips(self):
        return ()

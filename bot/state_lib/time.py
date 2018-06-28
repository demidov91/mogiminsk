import datetime
from typing import Tuple

from sqlalchemy import or_

from aiohttp_translation import gettext_lazy as _
from bot.messages.time import MorningMessage, DayMessage, EveningMessage
from bot.state_lib.base import BaseState
from messager.helper import Messager
from mogiminsk.defines import DATE_TIME_FORMAT
from mogiminsk.models import Trip
from mogiminsk.utils import get_db


import logging
logger = logging.getLogger(__name__)


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

    def _get_first_time(self):
        if self.messager == Messager.VIBER:
            return '6:30'

        return '6:00'

    def _get_last_time(self):
        if self.messager == Messager.VIBER:
            return '21:30'

        return '22:00'

    async def process(self):
        if self.value in ('morning', 'day', 'evening'):
            self.data['timeperiod'] = self.value
            return

        is_morning = False
        is_evening = False

        if self.value == MorningMessage.FIRST:
            is_morning = True
            time = self._get_first_time()

        elif self.value == EveningMessage.LAST:
            is_evening = True
            time = self._get_last_time()

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
            fetcher_class = MorningTripFetcher

        elif is_evening:
            fetcher_class = EveningTripFetcher

        else:
            if self.messager == Messager.VIBER:
                fetcher_class = ViberDefaultTripFetcher

            elif self.messager == Messager.TELEGRAM:
                fetcher_class = TelegramDefaultTripFetcher

            else:
                logger.error('Undefined messanger: %s', self.messager)
                fetcher_class = TelegramDefaultTripFetcher

        return fetcher_class(start_datetime, self.data['where']).produce()


class BaseTripFetcher:
    success = True

    big_start_datetime_range = None       # type: Tuple[datetime.timedelta, datetime.timedelta]
    small_start_datetime_range = None     # type: Tuple[datetime.timedelta, datetime.timedelta]

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
            lambda x: small_time_range[0] <= x.start_datetime < small_time_range[1],
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


class ViberDefaultTripFetcher(BaseTripFetcher):
    big_start_datetime_range = datetime.timedelta(hours=1), datetime.timedelta(hours=1)
    small_start_datetime_range = datetime.timedelta(minutes=15), datetime.timedelta(minutes=30)


class TelegramDefaultTripFetcher(BaseTripFetcher):
    big_start_datetime_range = datetime.timedelta(hours=2), datetime.timedelta(hours=2)
    small_start_datetime_range = datetime.timedelta(minutes=15), datetime.timedelta(minutes=60)


class MorningTripFetcher(BaseTripFetcher):
    """
    Returns first trips of the day.
    """
    big_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(minutes=-1)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(minutes=-1)


class EveningTripFetcher(BaseTripFetcher):
    """
    Returns last trips of the day.
    """
    big_start_datetime_range = datetime.timedelta(hours=0), datetime.timedelta(hours=3)
    small_start_datetime_range = datetime.timedelta(hours=0), datetime.timedelta(hours=3)


class ExtendedTripFetcher(BaseTripFetcher):
    big_start_datetime_range = datetime.timedelta(hours=6), datetime.timedelta(hours=8)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(hours=4)

    def no_trips(self):
        return ()

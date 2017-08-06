import datetime
from typing import Iterable

from mogiminsk.models import Trip
from bot_telegram.messages import BotMessage


class BaseMessageBuilder:
    def __init__(self, db):
        self.db = db

    def produce(self):
        raise NotImplementedError


class ShowMessageBuilder(BaseMessageBuilder):
    success = True
    message_caption = 'Choose a trip:'

    big_start_datetime_range = datetime.timedelta(hours=1), datetime.timedelta(hours=1)
    small_start_datetime_range = datetime.timedelta(minutes=10), datetime.timedelta(minutes=30)

    def __init__(self, dt: datetime.datetime, direction: str, db):
        super().__init__(db)
        self.dt = dt
        self.direction = direction

    def get_big_time_range(self):
        return

    def produce(self):
        big_time_range = self.dt - self.big_start_datetime_range[0],\
                         self.dt + self.big_start_datetime_range[1]
        small_time_range = self.dt - self.small_start_datetime_range[0],\
                           self.dt + self.small_start_datetime_range[1]

        trips_long_list = tuple(self.db.query(Trip).query(
            Trip.direction == self.direction).query(
            Trip.start_datetime._in(big_time_range)))

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

        trips = sorted(trips, key=self.trip_sorter)

        if len(trips) > 4:
            return self.build_message_with_extension(trips[:3], trips[3:])

        return self.build_simple_message(trips)

    def build_message_with_extension(self, initial_trips, extended_trips) -> BotMessage:
        buttons = [
            [self.trip_to_button(x)] for x in initial_trips
        ]
        buttons.append({
            'text': 'Show more',
            'data': 'show:[{}]'.format(','.join(str(x.id) for x in extended_trips)),
        })
        buttons.append({
            'text': 'Back',
            'data': 'back',
        })
        return BotMessage(text=self.message_caption, buttons=buttons)

    def build_simple_message(self, trips) -> BotMessage:
        buttons = [
            [self.trip_to_button(x)] for x in trips
        ]

        buttons.append({
            'text': 'Back',
            'data': 'back',
        })

        return BotMessage(text=self.message_caption, buttons=buttons)

    def trip_sorter(self, trip_1: Trip, trip_2: Trip):
        return trip_2.start_datetime > trip_1.start_datetime

    def trip_to_button(self, trip: Trip):
        text = '{}, {}'.format(
            trip.start_datetime.strftime('%H:%M'),
            trip.car.provider.name
        )

        return {
            'text': text,
            'data': trip.id,
        }

    def no_trips(self):
        return ExtendedShowMessageBuilder(self.dt, self.direction, self.db).produce()


class ExtendedShowMessageBuilder(ShowMessageBuilder):
    big_start_datetime_range = datetime.timedelta(hours=6), datetime.timedelta(hours=8)
    small_start_datetime_range = datetime.timedelta(hours=3), datetime.timedelta(hours=4)

    def no_trips(self):
        self.success = False
        return BotMessage(text='No trips was found')

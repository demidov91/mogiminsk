"""
Module with all states.
"""

import datetime
import re
from typing import Dict, Type

from bot_telegram.utils.telegram_helper import Message
from mogiminsk.defines import DATE_FORMAT
from mogiminsk.models import User
from .messages import BotMessage, DateBotMessage, OtherDateBotMessage

STATES = {}     # type: Dict[str, Type[BaseState]]


class BaseState:
    _intro_message = None    # type: BotMessage
    message_was_not_recognized = False
    is_callback_state = True

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()[:-5]

    def __init_subclass__(cls, **kwargs):
        super(BaseState, cls).__init_subclass__()
        STATES[cls.get_name()] = cls

    def __init__(self, update, request):
        self.update = update
        self.data = update.get_data() or {
            'state': self.get_name(),
        }
        self.value = self.get_value()
        self.request = request

    @classmethod
    def get_intro_message(cls):
        return cls._intro_message

    def get_value(self):
        return self.data.get(self.get_name())

    def get_state(self) -> str:
        return self.data['state']

    def set_state(self, state_name: str):
        self.data['state'] = state_name

    def consume(self, text: str):
        """
        Updates user state and sets *is_unrecognized* value.
        """
        raise NotImplementedError()

    def produce(self) ->BotMessage:
        next_state_class = STATES[self.get_state()]
        if not next_state_class.is_callback_state:
            self.set_db_state(self.get_state())

        message = next_state_class.get_intro_message()
        if self.message_was_not_recognized:
            return message.error_variant()

        return message

    def set_db_state(self, state: str):
        if self.request['user'] is None:
            telegram_user = self.update.get_user()
            if telegram_user is None or telegram_user.id is None:
                raise ValueError("Can't set db state to undefined user.")

            self.request['db'].add(User(
                telegram_id=telegram_user.id,
                telegram_state=state
            ))
        else:
            self.request['user'].state = state


class InitialState(BaseState):
    is_callback_state = False

    def consume(self, message: Message):
        self.set_state('where')


class WhereState(BaseState):
    """
    Store where we are going and ask WHEN?
    """
    _intro_message = BotMessage(
        text='Where are we going?',
        buttons=[[{
            'text': 'To Mogilev',
            'data': 'mogilev',
        }, {
            'text': 'To Minsk',
            'data': 'minsk',
        }]]
    )

    def consume(self, text: str):
        if self.value in ('mogilev', 'minsk'):
            self.set_state('date')

        else:
            self.message_was_not_recognized = True


class DateState(BaseState):
    """
    Store date of the trip.
    """
    @classmethod
    def get_intro_message(cls):
        return DateBotMessage()

    def consume(self, text: str):
        if self.value == 'back':
            self.set_state('where')
            return

        if self.value == 'other':
            self.set_state('otherdate')
            return

        try:
            datetime.datetime.strptime(self.value, DATE_FORMAT)
        except ValueError:
            self.message_was_not_recognized = True
            return

        self.set_state('time')


class OtherDateState(DateState):
    @classmethod
    def get_intro_message(cls):
        return OtherDateBotMessage()

    def consume(self, text: str):
        super(OtherDateState, self).consume(text)
        self.data[DateState.get_name()] = self.data[self.get_name()]


class TimeState(BaseState):
    _intro_message = BotMessage(
        text='Enter time. For example: 7, 1125 or 16:40.',
        buttons=[
            [{'data': 'back', 'text': 'Back'}]
        ],
    )

    time_pattern = re.compile('(?P<hours>\d{1,2}?):?(?P<minutes>\d{2})?\s*$')
    is_callback_state = False

    def consume(self, text: str):
        if self.value == 'back':
            self.set_state('date')
            return

        match = self.time_pattern.search(text)
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
        self.set_state('show')


class ShowState(BaseState):
    _intro_message = BotMessage(text='Not implemented yet')

    def consume(self, text: str):
        raise NotImplementedError()

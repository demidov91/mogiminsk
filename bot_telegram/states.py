"""
Module with all states.
"""

import datetime
import re
from typing import Dict, Type

from sqlalchemy.orm.attributes import flag_modified

from bot_telegram.utils.telegram_helper import Message
from mogiminsk.defines import DATE_FORMAT
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
        self.data = request['user'].telegram_context
        self.value = update.get_data()
        self.data[self.get_name()] = self.value
        self.request = request

    @classmethod
    def get_intro_message(cls, data):
        return cls._intro_message

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
        self.save_data()
        next_state_class = STATES[self.get_state()]
        message = next_state_class.get_intro_message(self.data)
        if self.message_was_not_recognized:
            return message.get_error_message()

        return message

    def save_data(self):
        self.request['user'].telegram_context = self.data
        flag_modified(self.request['user'], 'telegram_context')


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

    @classmethod
    def get_intro_message(cls, data):
        message = super().get_intro_message(data)

        if data.get('reset_reason'):
            message = message.copy()
            message.text = '{}\n{}'.format(data['reset_reason'], message.text)

        return message

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
    def get_intro_message(cls, data):
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
    def get_intro_message(cls, data):
        return OtherDateBotMessage()

    def consume(self, text: str):
        super(OtherDateState, self).consume(text)
        self.data[DateState.get_name()] = self.data[self.get_name()]

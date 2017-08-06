import datetime
import re
from typing import Dict, Type

from .util import Message
from mogiminsk.defines import DATE_FORMAT
from mogiminsk.models import User
from .messages import BotMessage, DateBotMessage, OtherDateBotMessage


STATES = {}     # type: Dict[str, Type[BaseState]]


class BaseState:
    _intro_message = None    # type: BotMessage
    message_was_not_recognized = False
    is_db_state = False

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()[:-5]

    def __init_subclass__(cls, **kwargs):
        super(BaseState, cls).__init_subclass__()
        STATES[cls.get_name()] = cls

    def __init__(self, data: dict, request):
        self.data = data
        self.value = self.get_value()
        self.request = request

    @classmethod
    def get_intro_message(cls):
        return cls._intro_message

    def get_value(self):
        return self.data.get(self.get_name())

    def consume(self, text: str):
        """
        Updates user state and sets *is_unrecognized* value.
        """
        raise NotImplementedError()

    def produce(self) ->BotMessage:
        next_state_class = STATES[self.data['state']]
        if next_state_class.is_db_state:
            self.set_db_state(self.data['state'])

        message = next_state_class.get_intro_message()
        if self.message_was_not_recognized:
            return message.error_variant()

        return message

    def set_db_state(self, state: str):
        if self.request['user'] is None:
            self.request['db'].add(User(
                telegam_id=None,
                telegram_state=state
            ))
        else:
            self.request['user'].state = state


class InitialState(BaseState):
    def consume(self, message: Message):
        self.data['state'] = 'where'


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
            self.data['state'] = 'date'

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
            self.data['state'] = 'where'
            return

        if self.value == 'other':
            self.data['state'] = 'otherdate'
            return

        try:
            datetime.datetime.strptime(self.value, DATE_FORMAT)
        except ValueError:
            self.message_was_not_recognized = True
            return

        self.data['state'] = 'time'


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
        text_buttons=('Back', ),
    )

    time_pattern = re.compile('(?P<hours>\d{1,2}?):?(?P<minutes>\d{2})?\s*$')
    is_db_state = True

    def consume(self, text: str):
        if text == 'Back':
            self.data['state'] = 'date'
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
        self.data['state'] = 'show'


class ShowState(BaseState):
    _intro_message = BotMessage(text='Not implemented yet')

    def consume(self, text: str):
        raise NotImplementedError()


def get_state(data, request) -> BaseState:
    return STATES[get_state_name(data, request)](data, request)


def get_state_name(data, request) -> str:
    """
    Get state name either from data or from db.
    """
    if data and ('state' in data) and (data['state'] in STATES):
        return data['state']

    if request['user'] is not None and request['user'].telegram_state:
        return request['user'].telegram_state

    return 'initial'


ERROR_MESSAGE = WhereState._intro_message.copy(
    text='Something went wrong...\n' + WhereState._intro_message.text
)



import datetime

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import DateBotMessage
from mogiminsk.defines import DATE_FORMAT


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

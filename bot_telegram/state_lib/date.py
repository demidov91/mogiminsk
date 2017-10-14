import datetime

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import DateBotMessage
from mogiminsk.defines import DATE_FORMAT


class DateState(BaseState):
    """
    Store date of the trip.
    """
    back = 'where'

    def get_intro_message(self):
        return DateBotMessage()

    async def process(self):
        if self.value == 'other':
            self.set_state('otherdate')
            return

        if self.value == '-':
            return

        try:
            datetime.datetime.strptime(self.value, DATE_FORMAT)
        except ValueError:
            self.message_was_not_recognized = True
            return

        self.set_state('time')

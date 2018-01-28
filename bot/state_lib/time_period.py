import datetime

from aiohttp_translation import gettext_lazy as _
from bot.state_lib.base import BaseState
from bot.messages.base import BotMessage, BACK
from mogiminsk.defines import DATE_FORMAT


class TimePeriodState(BaseState):
    back = 'date'

    MORNING_END = 11
    EVENING_START = 17

    TEXT = _('When?')
    BUTTONS = (
        {
            'text': _('\U0001f305 Morning'),
            'data': 'morning',
        },
        {
            'text': _('\U0001f31e Day'),
            'data': 'day',
        },
        {
            'text': _('\U0001f307 Evening'),
            'data': 'evening',
        },
    )

    def get_intro_message(self):
        current_time = datetime.datetime.now()

        if current_time.date() != datetime.datetime.strptime(self.data['date'], DATE_FORMAT):
            return BotMessage(self.TEXT, [self.BUTTONS, [BACK]])

        if current_time.hour < self.MORNING_END:
            return BotMessage(self.TEXT, [self.BUTTONS, [BACK]])

        if self.MORNING_END <= current_time.hour < self.EVENING_START:
            return BotMessage(self.TEXT, [self.BUTTONS[1:], [BACK]])

        return BotMessage(self.TEXT, [self.BUTTONS[2:], [BACK]])

    async def process(self):
        if self.value not in ('morning', 'day', 'evening'):
            self.message_was_not_recognized = True
            return

        self.set_state('time')

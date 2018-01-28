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
    buttons = (
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
        return BotMessage(self.TEXT, [self.buttons, [BACK]])

    async def initialize(self, current_state: str):
        current_time = datetime.datetime.now()

        if current_time.date() != datetime.datetime.strptime(self.data['date'], DATE_FORMAT).date():
            return self

        if current_time.hour < self.MORNING_END:
            return self

        if self.MORNING_END <= current_time.hour < self.EVENING_START:
            self.buttons = self.buttons[1:]
            return self

        if current_state == 'time':
            return await self.create_state('date').initialize(current_state)

        self.data['timeperiod'] = 'evening'
        return await self.create_state('time').initialize(current_state)

    async def process(self):
        if self.value not in ('morning', 'day', 'evening'):
            self.message_was_not_recognized = True
            return

        self.set_state('time')

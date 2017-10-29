from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from bot.state_lib.base import BaseState


class SeatState(BaseState):
    choices = tuple(range(1, 5))

    _intro_message = BotMessage(_('How many seats?'), buttons=[
        [{
            'text': str(x),
            'data': str(x),
        } for x in choices],
        [BACK]
    ])

    async def get_back_state(self):
        if self.data.get('seat'):
            return 'purchase'

        return 'show'

    async def process(self):
        try:
            seat_number = int(self.value)
        except ValueError:
            self.message_was_not_recognized = True
            return

        if seat_number not in self.choices:
            self.message_was_not_recognized = True
            return

        self.set_state('purchase')

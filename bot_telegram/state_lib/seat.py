from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other


class SeatState(BaseState):
    choices = tuple(range(1, 5))

    _intro_message = BotMessage('How many seats?', buttons=[
        [{
            'text': str(x),
            'data': str(x),
        } for x in choices],
        [{
            'text': 'Back',
            'data': 'back',
        }]
    ])

    async def process(self):
        try:
            seat_number = int(self.value)
        except ValueError:
            self.message_was_not_recognized = True
            return

        if seat_number not in self.choices:
            self.message_was_not_recognized = True
            return

        self.set_state(purchase_state_or_other(self.user, self.data))

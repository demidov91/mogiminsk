from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.models import Trip
from mogiminsk.services.user import UserService


class WhereState(BaseState):
    """
    Store where we are going and ask WHEN?
    """
    _intro_message = BotMessage(
        text='Where are we going?',
        buttons=[
            [{
                'text': 'To Mogilev',
                'data': Trip.MINSK_MOG_DIRECTION,
            }, {
                'text': 'To Minsk',
                'data': Trip.MOG_MINSK_DIRECTION,
            }],
            [
                {'text': 'My trips', 'data': 'purchase_list'}
            ]

        ]
    )

    def get_intro_message(self):
        message = super().get_intro_message().copy()
        if not UserService(self.user).future_purchases().count():
            message.buttons = message.buttons[:-1]

        return message

    async def process(self):
        if self.value in (Trip.MOG_MINSK_DIRECTION, Trip.MINSK_MOG_DIRECTION):
            self.set_state('date')
            return

        if self.value == 'purchase_list':
            self.set_state('purchaselist')
            return

        self.message_was_not_recognized = True
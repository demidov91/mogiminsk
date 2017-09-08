from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.models import Trip


class WhereState(BaseState):
    """
    Store where we are going and ask WHEN?
    """
    _intro_message = BotMessage(
        text='Where are we going?',
        buttons=[[{
            'text': 'To Mogilev',
            'data': Trip.MINSK_MOG_DIRECTION,
        }, {
            'text': 'To Minsk',
            'data': Trip.MOG_MINSK_DIRECTION,
        }]]
    )

    async def process(self):
        if self.value in (Trip.MOG_MINSK_DIRECTION, Trip.MINSK_MOG_DIRECTION):
            self.set_state('date')

        else:
            self.message_was_not_recognized = True
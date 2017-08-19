from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage


class PhoneState(BaseState):
    _intro_message = BotMessage(None, text_buttons=[[{
        'type': 'phone',
    }]])

    def consume(self, text: str):
        pass
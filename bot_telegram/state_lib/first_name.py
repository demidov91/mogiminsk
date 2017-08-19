from .base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other


class FirstNameState(BaseState):
    _intro_message = BotMessage(text="What's your name?", buttons=[[{
        'text': 'Back',
        'data': 'back',
    }]])

    def process(self):
        if self.text:
            self.text = self.text.strip()

        if not self.text:
            self.message_was_not_recognized = True
            return

        self.user.first_name = self.text
        self.set_state(purchase_state_or_other(self.user))

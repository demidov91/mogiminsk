from .base import BaseState
from bot_telegram.messages import BotMessage


class FirstNameState(BaseState):
    _intro_message = BotMessage(text="What's your name?", buttons=[[{
        'text': 'Back',
        'data': 'back',
    }]])

    async def process(self):
        if self.text:
            self.text = self.text.strip()

        if not self.text:
            self.message_was_not_recognized = True
            return

        self.user.first_name = self.text
        self.set_state('purchase')

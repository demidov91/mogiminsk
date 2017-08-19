from .base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other


class FirstNameState(BaseState):
    _intro_message = BotMessage(text="What's your name?")

    def consume(self, text: str):

        if text:
            text = text.strip()

        if not text:
            self.message_was_not_recognized = True
            return

        self.data[self.get_name()] = text
        self.set_state(purchase_state_or_other(self.user))

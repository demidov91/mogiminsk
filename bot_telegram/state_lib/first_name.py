from aiohttp_translation import gettext_lazy as _
from .base import BaseState
from bot.messages.base import BotMessage


class FirstNameState(BaseState):
    async def get_back_state(self):
        if self.user.first_name:
            return 'purchase'

        return 'show'

    _intro_message = BotMessage(text=_("What's your name?"), buttons=[[{
        'text': _('Back'),
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

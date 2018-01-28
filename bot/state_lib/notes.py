from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from bot.state_lib.base import BaseState


class NotesState(BaseState):
    back = 'purchase'

    _intro_message = BotMessage(_('Add some notes:'), buttons=[[BACK]], is_text_input=True)

    async def process(self):
        notes = (self.text or '').strip()
        self.data[self.get_name()] = notes
        self.set_state('purchase')

from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot.messages.base import BotMessage, BACK


class NotesState(BaseState):
    back = 'purchase'

    _intro_message = BotMessage(_('Add some notes:'), buttons=[[BACK]])

    async def process(self):
        notes = (self.text or '').strip()
        self.data[self.get_name()] = notes
        self.set_state('purchase')

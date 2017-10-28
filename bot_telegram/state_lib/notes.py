from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot.messages.base import BotMessage


class NotesState(BaseState):
    back = 'purchase'

    _intro_message = BotMessage(_('Add some notes:'), buttons=[[{
        'text': _('Back'),
        'data': 'back',
    }]])

    async def process(self):
        notes = (self.text or '').strip()
        self.data[self.get_name()] = notes
        self.set_state('purchase')

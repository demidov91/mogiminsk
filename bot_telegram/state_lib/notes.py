from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage


class NotesState(BaseState):
    _intro_message = BotMessage('Add some notes:', buttons=[[{
        'text': 'Back',
        'data': 'back',
    }]])

    async def process(self):
        notes = (self.text or '').strip()
        self.data[self.get_name()] = notes
        self.set_state('purchase')

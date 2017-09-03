from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other


class NotesState(BaseState):
    _intro_message = BotMessage('Add some notes:')

    def process(self):
        notes = (self.text or '').strip()
        self.data[self.get_name()] = notes
        self.set_state(purchase_state_or_other(self.user, self.data))

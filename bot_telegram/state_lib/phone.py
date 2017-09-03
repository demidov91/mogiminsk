from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.state_lib.utils import purchase_state_or_other


class PhoneState(BaseState):
    _intro_message = BotMessage(
        text='Tap the button below to share your phone number.',
        text_buttons=[[{
            'text': 'Share phone number',
            'type': 'phone',
        }]])

    def process(self):
        if self.contact is None or self.contact.identifier != self.user.telegram_id:
            self.back_to('trip')
            self.message_was_not_recognized = True
            return

        self.user.phone = self.contact.phone
        self.set_state(purchase_state_or_other(self.user, self.data))

from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage


class PhoneState(BaseState):
    _intro_message = BotMessage(
        text='Tap the button below to share your phone number.',
        text_buttons=[[{
            'text': 'Share phone number',
            'type': 'phone',
        }, {
            'text': 'Back',
            'type': 'text',
        }]])

    async def process(self):
        if self.text and self.text.lower() == 'back':
            self.set_state(self.back_to('show'))
            return

        if self.contact is None or self.contact.identifier != self.user.telegram_id:
            self.set_state(self.back_to('show'))
            self.message_was_not_recognized = True
            return

        self.user.phone = self.contact.phone
        self.set_state('purchase')

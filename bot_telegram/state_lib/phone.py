from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage


class PhoneState(BaseState):
    _intro_message = BotMessage(
        text=_('Tap the button below to share your phone number.'),
        text_buttons=[[{
            'text': _('Share phone number'),
            'type': 'phone',
        }, {
            'text': _('Back'),
            'type': 'text',
        }]])

    async def process(self):
        if self.text and self.text.lower() == 'back':
            self.set_state('show')
            return

        if self.contact is None or self.contact.identifier != self.user.telegram_id:
            self.set_state('show')
            self.message_was_not_recognized = True
            return

        self.user.phone = self.contact.phone
        self.set_state('purchase')

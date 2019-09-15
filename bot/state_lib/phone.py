import re
from typing import Optional

from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from bot.state_lib.base import BaseState


class PhoneState(BaseState):
    _intro_message = BotMessage(
        text=_('Tap the button below to share your phone number.'),
        buttons=[[{
            'text': _('Share phone number'),
            'type': 'phone',
        }, BACK]],
        is_tg_text_buttons=True
    )

    async def process(self):
        if self.text and self.text.lower() == 'back':
            self.set_state('show')
            return

        phone = (self.contact and self.contact.phone) or validate_phone(self.text)

        if phone is None:
            self.set_state('show')
            self.message_was_not_recognized = True
            return

        self.user.phone = phone
        self.set_state('purchase')


def validate_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None

    phone = re.sub(r'[^A-Za-z\d]', '', phone)

    match = re.search(r'(\d{12})', phone)
    if not match:
        return None

    return match.group(1)

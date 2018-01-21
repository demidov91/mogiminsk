from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from bot.state_lib.base import BaseState
from mogiminsk.models import User
from mogiminsk.services.user import UserService


class PhoneState(BaseState):
    _intro_message = BotMessage(
        text=_('Tap the button below to share your phone number.'),
        text_buttons=[[{
            'text': _('Share phone number'),
            'type': 'phone',
        }, BACK]])

    back = 'show'

    async def process(self):
        if self.text and self.text.lower() == 'back':
            self.set_state('show')
            return

        if self.contact is None or not self.contact.is_user_phone:
            self.set_state('show')
            self.message_was_not_recognized = True
            return

        existing_user = UserService.filter(User.phone == self.contact.phone).first()
        if existing_user is None:
            self.user.phone = self.contact.phone

        else:
            UserService(existing_user).merge_user(self.user)
            self.user = existing_user

        self.set_state('purchase')

from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot.messages.base import BotMessage, BACK
from bot_telegram.utils.helper import (
    CancelableStateMixin,
    cancel_purchase
)


class CancelPurchaseWithSmsState(CancelableStateMixin, BaseState):
    back = 'purchase'

    def get_intro_message(self):
        if self.is_wrong_sms():
            text = _('Wrong SMS code.')
            buttons = [[
                BACK,
                {'text': _('Send again'), 'data': 'resend', }
            ]]

        else:
            text = _('SMS was sent to +%s. Enter it.') % self.user.phone
            buttons = [[BACK]]

        return BotMessage(
            text=text,
            buttons=buttons,
        )

    async def process(self):
        if self.value == 'resend':
            await cancel_purchase(self.user, self.data)
            return

        if self.text is None:
            self.message_was_not_recognized = True
            return

        self.text = self.text.strip()

        if not (3 <= len(self.text) < 10):
            self.message_was_not_recognized = True
            return

        await self.cancellation(sms_code=self.text)

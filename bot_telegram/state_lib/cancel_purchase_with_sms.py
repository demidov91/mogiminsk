from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.utils.helper import generic_cancellation


class CancelPurchaseWithSmsState(BaseState):
    back = 'purchase'

    def get_intro_message(self):
        return BotMessage(
            text=f'SMS was sent to +{self.user.phone}. Enter it.',
            buttons=[[{'text': 'Back', 'data': 'back',}]],
        )

    async def process(self):
        if self.text is None:
            self.message_was_not_recognized = True
            return

        self.text = self.text.strip()

        if not (3 <= len(self.text) < 10):
            self.message_was_not_recognized = True
            return

        await generic_cancellation(self, sms_code=self.text)

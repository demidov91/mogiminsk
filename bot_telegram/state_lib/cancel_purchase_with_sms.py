from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.utils.helper import cancel_purchase
from mogiminsk_interaction.connectors.core import PurchaseResult


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

        connector = await cancel_purchase(self.user, self.data, sms_code=self.text)
        result = connector.get_result()

        
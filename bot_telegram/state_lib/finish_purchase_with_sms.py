from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from bot_telegram.utils.helper import purchase, store_purchase_event
from mogiminsk_interaction.connectors.core import PurchaseResult


class FinishPurchaseWithSmsState(BaseState):
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

        connector = await purchase(self.user, self.data, sms_code=self.text)
        result = connector.get_result()

        if result == PurchaseResult.SUCCESS:
            await store_purchase_event(self.user, self.data)
            self.set_state('where')
            self.add_message(connector.get_message())
            return

        self.set_state('show')
        self.add_message(connector.get_message() or 'Failed to purchase the trip. Try another provider.')

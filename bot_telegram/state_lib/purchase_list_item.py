from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import MyTripMessage
from mogiminsk.services import PurchaseService
from bot_telegram.utils.helper import CancelableStateMixin


class PurchaseListItemState(CancelableStateMixin, BaseState):
    back = 'purchaselist'

    def get_intro_message(self):
        return MyTripMessage(PurchaseService.get(self.data['purchaselist']).trip)

    async def process(self):
        if self.value == 'cancel':
            self.set_cancel_purchase_id(self.data['purchaselist'])
            await self.cancellation()

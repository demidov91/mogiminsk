from bot.external_api import CancelableStateMixin
from bot.messages.trip import MyTripMessage
from bot.state_lib.base import BaseState
from mogiminsk.services import PurchaseService


class PurchaseListItemState(CancelableStateMixin, BaseState):
    back = 'purchaselist'

    def get_intro_message(self):
        return MyTripMessage(PurchaseService.get(self.data['purchaselist']).trip)

    async def process(self):
        if self.value == 'cancel':
            self.set_cancel_purchase_id(self.data['purchaselist'])
            await self.cancellation()

import datetime
import re

from bot_telegram.state_lib.base import BaseState
from bot_telegram.utils.helper import cancel_purchase
from bot_telegram.messages import BotMessage
from mogiminsk.models import Purchase, Trip
from mogiminsk.defines import TIME_FORMAT, DATE_FORMAT
from mogiminsk.utils import get_db
from mogiminsk_interaction.connectors.core import CancellationResult


class PurchaseListState(BaseState):
    back = 'where'
    action_pattern = re.compile('(?P<action>\w+)_t(?P<trip_id>\d+)(_p(?P<purchase_id>\d+))?')

    async def get_trips(self):
        return self.user.purchases.join(Trip).filter(Trip.start_datetime > datetime.datetime.now())

    async def get_intro_message(self):
        purchases = tuple(await self.get_trips())
        if not purchases:
            return BotMessage('You have no pending trips')

        buttons = []
        for purchase in purchases:
            buttons.append([
                {
                    'text': purchase.trip.start_datetime.strftim(TIME_FORMAT + ' ' + DATE_FORMAT),
                    'data': 'show_t{}'.format(purchase.trip.id),
                },
                {
                    'text': b'\xE2\x9D\x8C'.decode('utf-8'),
                    'data': 'cancel_t{}_p{}'.format(purchase.trip.id, purchase.id),
                }
            ])

        buttons.append([{'text': 'Back', 'data': 'back'}])

        text = 'Your purchase' if len(purchases) > 1 else 'Your purchase'

        return BotMessage(text, buttons)

    async def process(self):
        if not self.value:
            self.message_was_not_recognized = True
            return

        match = self.action_pattern.match(self.value)
        if match is None:
            self.message_was_not_recognized = True
            return

        if match.group('action') == 'show':
            self.data['show'] = match.group('trip_id')
            self.set_state('trip')
            return

        if match.group('action') == 'cancel':
            self.data['purchase_cancel'] = match.group('purchase_id')

            connnector = await cancel_purchase(self.user, self.data)
            result = connnector.get_result()

            if result == CancellationResult.SUCCESS:
                self.add_message(connnector.get_message() or 'Purchase was CANCELLED!')
                return

            if result == CancellationResult.NEED_SMS:
                self.set_state('cancelpurchasewithsms')
                return

            if result == CancellationResult.DOES_NOT_EXIST:
                self.add_message('Looks like the purchasement was already cancelled. '
                                 'Call to the company if you dont think so.')
                self.data['show'] = match.group('trip_id')
                self.set_state('trip')
                return

            self.add_message(
                connnector.get_message() or
                'Failed to cancel. Please, call to the company to cancel.'
            )




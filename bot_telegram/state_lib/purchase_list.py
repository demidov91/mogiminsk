import re

from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot_telegram.utils.helper import CancelableStateMixin
from bot.messages.base import BotMessage, BACK
from mogiminsk.services.user import UserService
from mogiminsk.models import Trip
from mogiminsk.defines import TIME_FORMAT


class PurchaseListState(CancelableStateMixin, BaseState):
    back = 'where'
    action_pattern = re.compile('(?P<action>\w+)_(?P<purchase_id>\d+)?')

    def build_purchase_label(self, purchase):
        trip_time = purchase.trip.start_datetime.strftime(TIME_FORMAT)
        trip_date = purchase.trip.start_datetime.strftime('%d.%m')
        if purchase.trip.direction == Trip.MINSK_MOG_DIRECTION:
            trip_direction = _('Minsk-Mog.')

        elif purchase.trip.direction == Trip.MOG_MINSK_DIRECTION:
            trip_direction = _('Mog.-Minsk')

        else:
            trip_direction = ''

        return f'{trip_direction} {trip_time} {trip_date}'

    def get_intro_message(self):
        purchases = tuple(UserService(self.user).future_purchases())
        if not purchases:
            return BotMessage(
                _('You have no pending trips'),
                buttons=[[BACK]]
            )

        buttons = []
        for purchase in purchases:
            buttons.append([
                {
                    'text': self.build_purchase_label(purchase),
                    'data': 'show_{}'.format(purchase.id),
                },
                {
                    'text': b'\xE2\x9D\x8C'.decode('utf-8'),
                    'data': 'cancel_{}'.format(purchase.id),
                }
            ])

        buttons.append([BACK])

        text = _('Your purchases') if len(purchases) > 1 else _('Your purchase')

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
            self.data['purchaselist'] = match.group('purchase_id')
            self.set_state('purchaselistitem')
            return

        if match.group('action') == 'cancel':
            self.set_cancel_purchase_id(match.group('purchase_id'))
            await self.cancellation()

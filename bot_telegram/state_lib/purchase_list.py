import re

from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot_telegram.utils.helper import generic_cancellation
from bot_telegram.messages import BotMessage
from mogiminsk.services.user import UserService
from mogiminsk.defines import TIME_FORMAT, DATE_FORMAT


class PurchaseListState(BaseState):
    back = 'where'
    action_pattern = re.compile('(?P<action>\w+)_t(?P<trip_id>\d+)(_p(?P<purchase_id>\d+))?')

    def get_intro_message(self):
        purchases = tuple(UserService(self.user).future_purchases())
        if not purchases:
            return BotMessage(
                _('You have no pending trips'),
                buttons=[[{'text': _('Back'), 'data': 'back'}]]
            )

        buttons = []
        for purchase in purchases:
            buttons.append([
                {
                    'text': purchase.trip.start_datetime.strftime(TIME_FORMAT + ' ' + DATE_FORMAT),
                    'data': 'show_t{}'.format(purchase.trip.id),
                },
                {
                    'text': b'\xE2\x9D\x8C'.decode('utf-8'),
                    'data': 'cancel_t{}_p{}'.format(purchase.trip.id, purchase.id),
                }
            ])

        buttons.append([{'text': _('Back'), 'data': 'back'}])

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
            self.data['show'] = match.group('trip_id')
            self.set_state('trip')
            return

        if match.group('action') == 'cancel':
            self.data['purchase_cancel'] = match.group('purchase_id')
            await generic_cancellation(self)

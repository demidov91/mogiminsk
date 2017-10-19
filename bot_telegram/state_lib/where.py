from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.models import Trip
from mogiminsk.services.user import UserService


class WhereState(BaseState):
    """
    Store where we are going and ask WHEN?
    """
    with_trips_intro_message = BotMessage(
        text=_('Where are we going?'),
        buttons=[
            [{
                'text': _('To Mogilev'),
                'data': Trip.MINSK_MOG_DIRECTION,
            }, {
                'text': _('To Minsk'),
                'data': Trip.MOG_MINSK_DIRECTION,
            }],
            [
                {'text': _('My trips'), 'data': 'purchase_list'}
            ],
            [
                {'text': _('Feedback'), 'data': 'feedback',}
            ]
        ]
    )

    no_trips_intro_message = BotMessage(
        text=_('Where are we going?'),
        buttons=[
            [{
                'text': _('To Mogilev'),
                'data': Trip.MINSK_MOG_DIRECTION,
            }, {
                'text': _('To Minsk'),
                'data': Trip.MOG_MINSK_DIRECTION,
            }],
            [
                {'text': _('Feedback'), 'data': 'feedback',}
            ]
        ]
    )

    def get_intro_message(self):
        if not UserService(self.user).future_purchases().count():
            return self.no_trips_intro_message

        return self.with_trips_intro_message

    async def process(self):
        if self.value in (Trip.MOG_MINSK_DIRECTION, Trip.MINSK_MOG_DIRECTION):
            self.set_state('date')
            return

        if self.value == 'purchase_list':
            self.set_state('purchaselist')
            return

        if self.value == 'feedback':
            self.set_state('feedback')
            return

        self.message_was_not_recognized = True
from aiohttp_translation import gettext_lazy as _
from bot.messages.trip import PurchaseTripMessage
from bot.state_lib.base import BaseState
from mogiminsk.services.trip import TripService


class TripState(BaseState):
    back = 'show'

    def get_intro_message(self):
        trip = TripService.get(self.data['show'])
        return PurchaseTripMessage(trip)

    async def process(self):
        if self.value == 'finish':
            self.set_state('where')
            self.add_message(_(
                "I hope you've called dispatcher. "
                "Trips with \U0001f4de icons can't be booked from bot. "
                "Choose trip with \U0001f690 symbol to book in-app.")
            )
            return

        if self.value.startswith('tel:'):
            self.add_message(_('Press "Got it" button after you\'ve purchased the trip.'))
            return

        self.message_was_not_recognized = True

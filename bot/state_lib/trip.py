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
        if self.value == 'finish' or self.value.startswith('tel:'):
            self.set_state('where')
            self.add_message(
                _("I hope you've called dispatcher. "
                  "Trips with %s icons can't be booked from bot. "
                  "Choose trip with %s symbol to book in-app.") % (
                    b'\xF0\x9F\x93\x9E'.decode('utf-8'),
                    b'\xF0\x9F\x9A\x90'.decode('utf-8')
                )
            )
            return

        self.message_was_not_recognized = True

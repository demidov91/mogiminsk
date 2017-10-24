from aiohttp_translation import gettext_lazy as _
from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip
from mogiminsk.services.trip import TripService
from mogiminsk_interaction.utils import has_connector


class TripState(BaseState):
    back = 'show'

    @staticmethod
    def get_text(trip: Trip):
        trip_service = TripService(trip)

        contacts = filter(lambda x: x.kind in (
            'velcom', 'mts', 'life'
        ), trip_service.provider().contacts)

        contacts_message = '\n'.join(
            [f'{contact.kind}: {contact.contact}' for contact in contacts]
        )

        text = '{}, {}, {}'.format(
            trip_service.provider_name(),
            trip_service.direction_name(),
            trip.start_datetime.strftime('%d.%m.%Y %H:%M')
        )

        if not contacts_message:
            text += '\n' + _('Unfortunately I have no contacts for this trip :(')

        else:
            text += ':\n' + contacts_message

        return text

    @staticmethod
    def get_buttons(trip):
        if has_connector(trip.car.provider.identifier):
            return [
                [{
                    'text': _('Back'),
                    'data': 'back',
                }, {
                    'text': _('Book it'),
                    'data': 'purchase',
                }],
                [{
                    'text': _('Got it'),
                    'data': 'finish',
                }]
            ]

        return [
            [{
                'text': _('Back'),
                'data': 'back',
            }, {
                'text': _('Got it'),
                'data': 'finish',
            }]
        ]

    def get_intro_message(self):
        trip = TripService.get(self.data['show'])
        return BotMessage(
            text=self.get_text(trip),
            buttons=self.get_buttons(trip),
        )

    async def process(self):
        if self.value == 'finish':
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

        if self.value == 'purchase':
            self.set_state('purchase')
            return

        self.message_was_not_recognized = True

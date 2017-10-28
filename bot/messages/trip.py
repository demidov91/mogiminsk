from typing import List

from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from mogiminsk.services import TripService
from mogiminsk_interaction.utils import has_connector


class TripMessage(BotMessage):
    def __init__(self, trip):
        self.trip = trip
        super().__init__()

    def build_text(self, text: str):
        trip_service = TripService(self.trip)

        contacts = filter(lambda x: x.kind in (
            'velcom', 'mts', 'life'
        ), trip_service.provider().contacts)

        contacts_message = '\n'.join(
            [f'{contact.kind}: {contact.contact}' for contact in contacts]
        )

        text = '{}, {}, {}'.format(
            trip_service.provider_name(),
            trip_service.direction_name(),
            self.trip.start_datetime.strftime('%d.%m.%Y %H:%M')
        )

        if not contacts_message:
            text += '\n' + _('Unfortunately I have no contacts for this trip :(')

        else:
            text += ':\n' + contacts_message

        return text


class PurchaseTripMessage(TripMessage):
    def build_callback_buttons(self, buttons: List[List[dict]]):
        if has_connector(self.trip.car.provider.identifier):
            return [
                [BACK,
                 {
                    'text': _('Book it'),
                    'data': 'purchase',
                }],
                [{
                    'text': _('Got it'),
                    'data': 'finish',
                }]
            ]

        return [
            [BACK,
             {
                'text': _('Got it'),
                'data': 'finish',
            }]
        ]


class MyTripMessage(TripMessage):
    def build_callback_buttons(self, buttons: List[List[dict]]):
        return [
            [{
                'text': _('⬅ Back'),
                'data': 'back',
            }, {
                'text': _('Cancel ❌'),
                'data': 'cancel',
            }]
        ]

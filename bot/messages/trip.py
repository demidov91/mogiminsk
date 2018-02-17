from typing import List

from aiohttp_translation import gettext_lazy as _
from bot.messages.base import BotMessage, BACK
from mogiminsk.services import TripService
from mogiminsk_interaction.utils import has_connector


class TripMessage(BotMessage):
    def __init__(self, trip, **kwargs):
        self.trip_id = trip.id
        self.trip_service = TripService(trip)
        super().__init__(**kwargs)

    def _get_contacts(self):
        return filter(lambda x: x.kind in (
            'velcom', 'mts', 'life'
        ), self.trip_service.provider().contacts)

    def build_text(self, text: str):
        contacts = self._get_contacts()

        contacts_message = '\n'.join(
            [f'{contact.kind}: {contact.contact}' for contact in contacts]
        )

        text = '{}, {}, {}'.format(
            self.trip_service.provider_name(),
            self.trip_service.direction_name(),
            self.trip_service.instance.start_datetime.strftime('%d.%m.%Y %H:%M')
        )

        if not contacts_message:
            text += '\n' + _('Unfortunately I have no contacts for this trip :(')

        else:
            text += ':\n' + contacts_message

        return text


class PurchaseTripMessage(TripMessage):
    def build_callback_buttons(self, buttons: List[List[dict]]):
        return [
            [BACK,
             {
                'text': _('Got it'),
                'data': 'finish',
            }]
        ]

    def get_viber_buttons(self):
        self.trip_service = TripService.get_service(self.trip_id)

        contacts = self._get_contacts()

        phone_numbers = [{
            'text': f'{x.kind}: {x.contact}',
            'data': f'tel:{x.contact}',
            'type': 'url',
        } for x in contacts]
        return phone_numbers + super().get_viber_buttons()


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

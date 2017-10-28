from copy import deepcopy
import datetime
from typing import List, Dict, Sequence

from babel.dates import format_date

from aiohttp_translation import gettext_lazy as _, get_active
from mogiminsk.defines import DATE_FORMAT
from mogiminsk.services import TripService
from mogiminsk_interaction.utils import has_connector


class BotMessage:
    def __init__(self,
                 text: str='',
                 buttons: List[List[Dict]]=None,
                 text_buttons: List[List[str]]=None,
                 parse_mode: str = None):
        self.text = self.build_text(text)
        self.parse_mode = parse_mode
        self.buttons = self.build_callback_buttons(buttons)
        self.text_buttons = self.build_text_buttons(text_buttons)

    def copy(self, text=None, parse_mode=None, buttons=None) ->'BotMessage':
        if text is None:
            text = self.text

        if buttons is None:
            buttons = self.buttons

        if parse_mode is None:
            parse_mode = self.parse_mode

        copy = BotMessage(
            text=text,
            parse_mode=parse_mode,
            buttons=deepcopy(buttons),
        )
        return copy

    def to_sequence(self, prepend_messages: List[str]=()) -> Sequence['BotMessage']:
        messages = [BotMessage(x) for x in prepend_messages]
        messages.append(self)
        return messages

    def build_text(self, text: str) ->str:
        return text

    def build_callback_buttons(self, buttons: List[List[dict]]) ->List[List[dict]]:
        return buttons

    def build_text_buttons(self, buttons: List[List[str]]) ->List[List[str]]:
        return buttons


class DateMessage(BotMessage):
    def __init__(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        buttons = (
            (
                _('Today, %s') % format_date(today, 'E', locale=get_active()),
                today.strftime(DATE_FORMAT)
            ),
            (
                _('Tomorrow, %s') % format_date(tomorrow, 'E', locale=get_active()),
                tomorrow.strftime(DATE_FORMAT)
            ),
            (
                _('Other'),
                'other'
            ),
        )
        buttons = [
            [{'text': x[0], 'data': x[1]} for x in buttons],
            [{'text': _('Back'), 'data': 'back',}],
        ]

        super(DateMessage, self).__init__(_('Choose the date'), buttons)


class OtherDateMessage(BotMessage):
    def _date_to_button(self, date: datetime.date):
        return {
            'text': str(date.day),
            'data': date.strftime(DATE_FORMAT),
        }

    def __init__(self):
        today = datetime.date.today()
        weekday = today.weekday()

        first_line = [{
            'text': b'\xE2\x9D\x8C'.decode('utf-8'),
            'data': '-',
        } for _ in range(weekday)]

        first_line.extend(
            self._date_to_button(today + datetime.timedelta(days=x))
            for x in range(7 - weekday)
        )
        second_line = [
            self._date_to_button(today + datetime.timedelta(days=x))
            for x in range(7 - weekday, 14 - weekday)
        ]

        buttons = [
            first_line,
            second_line,
            [{'text': _('Back'), 'data': 'back', }],
        ]

        super(OtherDateMessage, self).__init__(_('Choose the date'), buttons)


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



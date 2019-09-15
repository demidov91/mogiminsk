from sqlalchemy import and_

from aiohttp_translation import gettext_lazy as _
from bot.external_api import purchase, store_purchase_event
from bot.messages.base import BotMessage
from bot.state_lib.base import BaseState
from mogiminsk.models import Trip, Purchase, Car, Provider
from mogiminsk.services.trip import TripService
from mogiminsk.utils import get_db
from mogiminsk_interaction.connectors.core import PurchaseResult


class PurchaseState(BaseState):
    connector = None
    back = 'show'

    async def initialize(self, current_state):
        if current_state in ('trip', 'show'):
            self.data.pop('seat', None)
            self.data.pop('station', None)
            self.data.pop('notes', None)

        if not self.user.phone:
            return await self.create_state('phone').initialize(current_state)

        if not self.user.first_name:
            return await self.create_state('firstname').initialize(current_state)

        if 'station' not in self.data:
            self._initialize_station()
            if 'station' not in self.data:
                return await self.create_state('station').initialize(current_state)

        if 'seat' not in self.data:
            self._initialize_seat()
            if 'seat' not in self.data:
                return await self.create_state('seat').initialize(current_state)

        return await super().initialize(current_state)

    def _initialize_station(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['show'])

        last_purchase = db.query(Purchase).join(Trip, Car, Provider).filter(and_(
            Trip.direction == trip.direction,
            Purchase.user_id == self.user.id,
            Provider.id == trip.car.provider_id,
        )).first()
        if last_purchase is None:
            return

        self.data['station'] = last_purchase.station.id
        self.data['station_name'] = last_purchase.station.name

    def _initialize_seat(self):
        db = get_db()

        last_purchase = db.query(Purchase).filter(
            Purchase.user_id == self.user.id
        ).order_by(Purchase.created_at.desc()).first()

        if last_purchase is None:
            return

        self.data['seat'] = last_purchase.seats

    def get_text(self, trip: Trip):
        trip_service = TripService(trip)

        return _(
            'Firm: %(provider)s\n'
            'Direction: %(direction)s\n'
            'Time: %(time)s\n'
            'Phone: %(phone)s\n'
            '(Tap on the buttons bellow to change)'
        ) % {
            'provider': trip_service.provider_name(),
            'direction': trip_service.direction_name(),
            'time': trip_service.instance.start_datetime,
            'phone': self.user.phone,
        }

    def get_buttons(self):
        notes = self.data.get('notes')
        notes = _('Notes: %s') % notes if notes else _('Notes')

        return [
            [{'text': _('Name: %s') % self.user.first_name, 'data': 'firstname'}],
            [{'text': _('Phone: +%s') % self.user.phone, 'data': 'phone'}],
            [{'text': _('Pick up: %s') % self.data["station_name"], 'data': 'station'}],
            [{'text': _('%s seat(s)') % self.data["seat"], 'data': 'seat'}],
            [{'text': notes, 'data': 'notes'}],
            [
                {'text': _('⬅️ Back'), 'data': 'back'},
                {'text': _('Book it! ✅'), 'data': 'submit'},
            ],
        ]

    def get_intro_message(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['show'])

        return BotMessage(
            text=self.get_text(trip),
            buttons=self.get_buttons()
        )

    async def process(self):
        if self.value in ('firstname', 'phone', 'station', 'seat', 'notes'):
            self.set_state(self.value)
            return

        if self.value == 'submit':
            connector = await purchase(self.user, self.data)
            purchase_result = connector.get_result()
            if purchase_result == PurchaseResult.SUCCESS:
                self.add_message(connector.get_message())
                self.set_state('where')
                await store_purchase_event(self.user, self.data)
                return

            if purchase_result == PurchaseResult.FAIL:
                self.set_state('show')
                self.add_message(_('Failed to purchase the trip. Try another provider.'))
                return

            if purchase_result == PurchaseResult.NEED_REGISTRATION:
                self.set_state('finishpurchasewithsms')
                return

        self.message_was_not_recognized = True

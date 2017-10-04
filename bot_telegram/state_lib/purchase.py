from sqlalchemy import and_

from bot_telegram.state_lib.base import BaseState
from bot_telegram.utils.helper import purchase, store_purchase_event
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip, Purchase, Car, Provider
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
        return f'Firm: {trip.car.provider.name}\n' \
               f'Direction: {trip.direction}\n' \
               f'Time: {trip.start_datetime}\n' \
               f'Phone: {self.user.phone}\n' \
               f'(Tap on the buttons bellow to change)'

    def get_buttons(self):
        notes = self.data.get('notes')
        notes = f'Notes: {notes}' if notes else 'Notes'

        return [
            [{'text': f'Name: {self.user.first_name}', 'data': 'firstname'}],
            [{'text': f'Pick up: {self.data["station_name"]}', 'data': 'station'}],
            [{'text': f'{self.data["seat"]} seat(s)', 'data': 'seat'}],
            [{'text': f'{notes}', 'data': 'notes'}],
            [
                {'text': 'Back', 'data': 'back'},
                {'text': 'Book it!', 'data': 'submit'},
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
        if self.value in ('firstname', 'station', 'seat', 'notes'):
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
                self.add_message('Failed to purchase the trip. Try another provider.')
                return

            if purchase_result == PurchaseResult.NEED_REGISTRATION:
                self.set_state('finishpurchasewithsms')
                return

        self.message_was_not_recognized = True

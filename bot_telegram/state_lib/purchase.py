from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip, Purchase, Station
from mogiminsk_interaction.utils import get_connector
from mogiminsk_interaction.connectors.core import PurchaseResult


class PurchaseState(BaseState):
    connector = None

    def get_text(self, trip: Trip):
        return f'Firm: {trip.car.provider.name}\n' \
               f'Direction: {trip.direction}' \
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
                {'text': 'Purchase!', 'data': 'submit'},
            ],
        ]

    def get_intro_message(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['show'])

        return BotMessage(
            text=self.get_text(trip),
            buttons=self.get_buttons()
        )

    async def process_back(self):
        self.set_state(self.back_to('trip'))

    async def _purchase(self):
        db = get_db()

        trip = db.query(Trip).get(self.data['show'])
        station = db.query(Station).get(self.data['station'])

        self.connector = get_connector(trip.car.provider.identifier)

        return await self.connector.purchase(
            start_datetime=trip.start_datetime,
            direction=self.data['where'],
            seat=int(self.data['seat']),
            first_name=self.user.first_name,
            station=station.identifier,
            notes=self.data.get('notes'),
            phone=self.user.phone,
        )

    def _store_purchase_event(self):
        trip_id = int(self.data['show'])
        seat = int(self.data['seat'])
        station_id = int(self.data['station'])
        notes = self.data.get('notes')

        purchase = Purchase(
            trip_id=trip_id,
            seats=seat,
            station_id=station_id,
            notes=notes,
            user=self.user
        )

        get_db().add(purchase)

    async def process(self):
        if self.value in ('firstname', 'station', 'seat', 'notes'):
            self.set_state(self.value)
            return

        if self.value == 'submit':
            purchase_result = await self._purchase()
            if purchase_result == PurchaseResult.SUCCESS:
                self.add_message(self.connector.get_message())
                self.set_state(self.back_to('where'))
                self._store_purchase_event()
                return

            if purchase_result == PurchaseResult.FAIL:
                self.back_to('show')
                self.add_message('Failed to purchase the trip. Try another provider.')
                return

            if purchase_result == PurchaseResult.NEED_REGISTRATION:
                self.back_to('show')
                self.add_message(
                    "Sorry. Can't purchase your trip at the moment."
                    "Call to purchase the trip."
                )
                return

        self.message_was_not_recognized = True

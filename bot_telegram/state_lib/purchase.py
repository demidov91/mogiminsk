from bot_telegram.state_lib.base import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip, User


class PurchaseState(BaseState):
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

    def process_back(self):
        self.set_state(self.back_to('trip'))

    def process(self):
        if self.value in ('firstname', 'station', 'seat', 'notes'):
            self.set_state(self.value)
            return

        if self.value == 'submit':
            pass

        self.message_was_not_recognized = True

from bot_telegram.state_lib.base import BaseState
from bot_telegram.state_lib.utils import purchase_state_or_other
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip
from mogiminsk_interaction.utils import has_connector


class TripState(BaseState):
    @staticmethod
    def get_text(trip: Trip):
        contacts = filter(lambda x: x.kind in (
            'velcom', 'mts', 'life'
        ), trip.car.provider.contacts)

        contacts_message = '\n'.join(
            [f'{contact.kind}: {contact.contact}' for contact in contacts]
        )

        text = '{}, {}, {}'.format(
            trip.car.provider.name,
            trip.direction,
            trip.start_datetime.strftime('%d.%m.%Y %H:%M')
        )

        if not contacts_message:
            text += '\nUnfortunately I have no contacts for this trip :('

        else:
            text += ':\n' + contacts_message

        return text

    @staticmethod
    def get_buttons(trip):
        if has_connector(trip.car.provider.identifier):
            return [
                [{
                    'text': 'Back',
                    'data': 'back',
                }, {
                    'text': 'Purchase',
                    'data': 'purchase',
                }],
                [{
                    'text': 'Got it',
                    'data': 'finish',
                }]
            ]

        return [
            [{
                'text': 'Back',
                'data': 'back',
            }, {
                'text': 'Got it',
                'data': 'finish',
            }]
        ]

    def get_intro_message(self):
        db = get_db()
        trip = db.query(Trip).get(self.data['show'])
        return BotMessage(
            text=self.get_text(trip),
            buttons=self.get_buttons(trip),
        )

    def process(self):
        if self.value == 'finish':
            self.set_state('where')
            self.add_message('This is a beta-version, trip was not booked.')
            return

        if self.value == 'purchase':
            self.set_state(purchase_state_or_other(self.user, self.data))
            return

        self.message_was_not_recognized = True

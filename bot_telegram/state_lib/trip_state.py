from bot_telegram.states import BaseState
from bot_telegram.messages import BotMessage
from mogiminsk.utils import get_db
from mogiminsk.models import Trip


class TripStateMixin:
    prev_state_name = None  # type:str

    @classmethod
    def get_intro_message(cls, data):
        db = get_db()
        trip = db.query(Trip).get(Trip.id == data[cls.prev_state_name])
        contacts = filter(lambda x: x.kind in (
            'velcom', 'mts', 'life'
        ), trip.contacts)

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

        buttons = [
            [{
                'text': 'Back',
                'data': 'back',
            }, {
                'text': 'Got it',
                'data': 'finish',
            }]
        ]

        return BotMessage(
            text=text,
            buttons=buttons
        )

    def consume(self):
        if self.value == 'back':
            self.set_state(self.prev_state_name)
            return

        if self.value == 'finish':
            self.set_state('where')
            self.data['reset_reason'] = 'This is a beta-version, trip was not booked.'
            return


class TripAfterFullState(TripStateMixin, BaseState):
    prev_state_name = 'showfull'


class TripAfterShortState(TripStateMixin, BaseState):
    prev_state_name = 'showsplit'
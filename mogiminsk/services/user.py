import datetime

from ..models import User, Trip
from .base import BaseService


class UserService(BaseService):
    model = User

    messenger_fields = (
        ('telegram_id', 'telegram_context'),
        ('viber_id', 'viber_context'),
    )

    @classmethod
    def get_by_viber_id(self, viber_id):
        return self.filter(User.viber_id == viber_id).first()

    def future_purchases(self):
        return self.instance.purchases.join(Trip).filter(
            Trip.start_datetime > datetime.datetime.now()
        )

    def delete_purchase(self, purchase_id):
        self.instance.purchases.filter_by(id=purchase_id).delete()

    def merge_user(self, other: User):
        for messenger in self.messenger_fields:
            if getattr(other, messenger[0]):
                break

        else:
            raise ValueError('Unknown messenger to merge.')

        for field in messenger:
            setattr(self.instance, field, getattr(other, field))

        self.db().delete(other)

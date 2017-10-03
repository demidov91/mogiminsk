import datetime

from ..models import User, Trip
from .base import BaseService


class UserService(BaseService):
    model = User

    def future_purchases(self):
        return self.instance.purchases.join(Trip).filter(
            Trip.start_datetime > datetime.datetime.now()
        )

    def delete_purchase(self, purchase_id):
        self.instance.purchases.filter_by(id=purchase_id).delete()

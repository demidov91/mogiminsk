from typing import Iterable

from sqlalchemy import and_

from aiohttp_translation import gettext_lazy as _
from mogiminsk.services.base import BaseService
from mogiminsk.models import Trip, Station, Provider


class TripService(BaseService):
    model = Trip

    def provider(self):
        return self.instance.car.provider

    def provider_name(self):
        return self.instance.car.provider.name

    def provider_short_name(self):
        return self.instance.car.provider.short_name

    def direction_name(self):
        if self.instance.direction == Trip.MOG_MINSK_DIRECTION:
            return _('Mogilev - Minsk')

        if self.instance.direction == Trip.MINSK_MOG_DIRECTION:
            return _('Minsk - Mogilev')

        return self.instance.direction

    def get_stations(self) ->Iterable[Station]:
        return self.db().query(Station).join(Provider).filter(
            and_(
                Provider.id == self.instance.car.provider_id,
                Station.direction == self.instance.direction,
                Station.is_removed == False
            )
        )

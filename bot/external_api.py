"""
Helper module to use FROM state classes.
"""
import logging

from aiohttp_translation import gettext_lazy as _
from mogiminsk.models import Trip
from mogiminsk.services import UserService, PurchaseService, TripService, StationService
from mogiminsk_interaction.utils import get_connector
from mogiminsk_interaction.connectors.core import BaseConnector, CancellationResult


logger = logging.getLogger(__name__)


class SmsStorage:
    def __init__(self, context):
        self.context = context

    def _get_sms_key(self, trip: Trip=None, car=None, provider=None, provider_identifier=None) -> str:
        if provider_identifier:
            identifier = provider_identifier

        elif provider:
            identifier = provider.identifier

        elif car:
            identifier = car.provider.identifier

        elif trip:
            identifier = trip.car.provider.identifier

        else:
            raise ValueError()

        return f'sms_{identifier}'

    def get_sms_code(self, trip):
        return self.context.get(self._get_sms_key(trip=trip))

    def set_sms_code(self, code, trip=None, car=None, provider=None, provider_identifier=None):
        self.context[self._get_sms_key(
            trip=trip, car=car, provider=provider, provider_identifier=provider_identifier
        )] = code


class CancelableStateMixin:
    WRONG_SMS_KEY = 'cancelpurchasewithsms_wrong'

    def set_wrong_sms(self, is_wrong=True):
        self.data[self.WRONG_SMS_KEY] = is_wrong

    def is_wrong_sms(self) ->bool:
        return self.data.get(self.WRONG_SMS_KEY)

    def set_cancel_purchase_id(self, id):
        self.data['purchase_cancel'] = id

    def get_cancellation_trip_id(self):
        return self.data.get('purchase_cancel')

    async def cancellation(self, sms_code=None):
        """
        Makes external API cancellation call to cancel self.data['purchase_cancel'] trip
            and moves current state either to CancelWithSMS or to PurchaseList.
        :param sms_code: just entered SMS-code if any.
        """
        connector = await cancel_purchase(self.user, self.data, sms_code)
        result = connector.get_result()
        user_service = UserService(self.user)
        self.set_wrong_sms(False)

        if result == CancellationResult.SUCCESS:
            user_service.delete_purchase(self.get_cancellation_trip_id())
            self.set_state('purchaselist')
            self.add_message(connector.get_message() or _('Purchase was CANCELLED!'))
            return

        if result == CancellationResult.NEED_SMS:
            self.set_state('cancelpurchasewithsms')
            return

        if result == CancellationResult.WRONG_SMS:
            self.set_wrong_sms()
            self.set_state('cancelpurchasewithsms')
            return

        if result == CancellationResult.DOES_NOT_EXIST:
            self.add_message(_(
                "Looks like the purchasement was already cancelled. "
                "Call the company if you don't think so."
            ))
            user_service.delete_purchase(self.get_cancellation_trip_id())
            self.set_state('purchaselist')
            return

        self.add_message(
            connector.get_message() or
            _('Failed to cancel. Please, call the company to cancel.')
        )


async def purchase(user, context: dict, sms_code: str=None) ->BaseConnector:
    trip = TripService.get(context['show'])
    station = StationService.get(context['station'])

    connector = get_connector(trip.car.provider.identifier)

    await connector.purchase(
        start_datetime=trip.start_datetime,
        external_identifier=trip.external_identifier,
        direction=context['where'],
        seat=int(context['seat']),
        first_name=user.first_name,
        station=station.identifier,
        notes=context.get('notes'),
        phone=user.phone,
        sms_code=sms_code,
    )

    await connector.close()
    return connector


async def cancel_purchase(user, context, sms_code=None) ->BaseConnector:
    """
    Makes external API cancel call for the :context:['purchase_cancel'] trip.
    :return: External API connector with a result set.
    """

    trip = PurchaseService.get(context['purchase_cancel']).trip
    sms_storage = SmsStorage(user.external)
    sms_was_expicitely_set = sms_code is not None

    if sms_code:
        sms_storage.set_sms_code(sms_code, trip=trip)

    else:
        sms_code = sms_storage.get_sms_code(trip=trip)

    connector = get_connector(trip.car.provider.identifier)
    connector.sms_code = sms_code
    await connector.cancel_purchase(
        user.phone, trip.start_datetime, trip.direction, trip.car.name
    )

    if connector.result is CancellationResult.NEED_SMS:
        sms_storage.set_sms_code(None, trip=trip)

    elif connector.result is CancellationResult.WRONG_SMS:
        logger.info('Cancellation SMS %s has expired.', sms_code)
        if not sms_was_expicitely_set:
            sms_storage.set_sms_code(None, trip=trip)
            if sms_code:
                await connector.close()
                return await cancel_purchase(user, context)

            logger.error("Got WRONG_SMS result for a None SMS. It shouldn't happen!")

    await connector.close()

    return connector


async def store_purchase_event(user, context):
    trip_id = int(context['show'])
    seat = int(context['seat'])
    station_id = int(context['station'])
    notes = context.get('notes')

    PurchaseService.add(
        trip_id=trip_id,
        seats=seat,
        station_id=station_id,
        notes=notes,
        user=user
    )

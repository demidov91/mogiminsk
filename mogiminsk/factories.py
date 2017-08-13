import factory
from factory.alchemy import SQLAlchemyModelFactory
from .models import Provider, Car, Trip, User
from .utils import threaded_session


class ProviderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Provider
        sqlalchemy_session = threaded_session

    id = factory.Sequence(lambda x: x)
    identifier = factory.LazyAttribute(lambda x: 'provider-%d' % x.id)
    name = factory.LazyAttribute(lambda x: 'Provider %d' % x.id)


class CarFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Car
        sqlalchemy_session = threaded_session

    id = factory.Sequence(lambda x: x)
    provider = factory.SubFactory(ProviderFactory)
    name = factory.LazyAttribute(lambda x: 'Car %d' % x.id)
    kind = Car.MINIBUS_KIND


class TripFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Trip
        sqlalchemy_session = threaded_session

    id = factory.Sequence(lambda x: x)
    car = factory.SubFactory(CarFactory)
    direction = Trip.MOG_MINSK_DIRECTION


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = threaded_session

    telegram_id = factory.Sequence(lambda x: x)

    # ... or you can use Meta.force_flush=True
    telegram_context = {}

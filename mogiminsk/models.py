from sqlalchemy import Column, Integer, String, ForeignKey, \
    JSON, SmallInteger, DateTime, UniqueConstraint, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func


class TimeTrackingBase:
    created_at = Column(DateTime, nullable=True,
                        server_default=func.now())
    last_modified = Column(DateTime, nullable=True,
                           server_default=func.now(), server_onupdate=func.now())


Base = declarative_base(cls=TimeTrackingBase)


class User(Base):
    __tablename__ = 'mogiminsk_user'
    id = Column(Integer, primary_key=True)
    phone = Column(String(12), nullable=True, unique=True)
    first_name = Column(String(31), nullable=True)
    language = Column(String(5), nullable=True)
    external = Column(JSON, default={})

    telegram_context = Column(JSON, default={})
    telegram_id = Column(Integer, nullable=True, unique=True)
    telegram_state = Column(String(31), nullable=True)
    telegram_messages = Column(String(1023), nullable=True, default='')

    viber_context = Column(JSON, default={})
    viber_id = Column(Integer, nullable=True, unique=True)
    viber_state = Column(String(31), nullable=True)
    viber_messages = Column(String(1023), nullable=True, default='')

    purchases = relationship('Purchase', back_populates='user', lazy='dynamic')
    conversation = relationship('Conversation', back_populates='user', lazy='dynamic')


class Provider(Base):
    __tablename__ = 'mogiminsk_provider'
    id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)
    identifier = Column(String(15), nullable=False, unique=True)

    cars = relationship('Car', back_populates='provider')
    contacts = relationship('ProviderContact', back_populates='provider')
    stations = relationship('Station', back_populates='provider')


class ProviderContact(Base):
    __tablename__ = 'mogiminsk_provider_contact'

    VELCOM_KIND = 'velcom'
    MTS_KIND = 'mts'
    LIFE_KIND = 'life'
    WEB_KIND = 'web'

    id = Column(Integer, primary_key=True)
    contact = Column(String(63), nullable=False)
    kind = Column(String(15), nullable=False)

    provider_id = Column(Integer, ForeignKey(Provider.id), nullable=False)
    provider = relationship('Provider', back_populates='contacts')


class Car(Base):
    __tablename__ = 'mogiminsk_car'
    __table_args__ = UniqueConstraint('provider_id', 'name'),

    MINIBUS_KIND = 'minibus'
    BUS_KIND = 'bus'
    TRAIN_KIND = 'train'

    id = Column(Integer, primary_key=True)

    provider_id = Column(Integer, ForeignKey(Provider.id), nullable=False)
    provider = relationship('Provider', back_populates='cars')

    name = Column(String(127), nullable=False)
    kind = Column(String(7), nullable=False)

    trips = relationship('Trip', back_populates='car')

    def __str__(self):
        if self.id:
            return '{}. {}.'.format(self.name, self.provider.name)
        return 'Not saved name={} Car instance'.format(self.name)


class Trip(Base):
    __tablename__ = 'mogiminsk_trip'

    MOG_MINSK_DIRECTION = 'mogilev-minsk'
    MINSK_MOG_DIRECTION = 'minsk-mogilev'

    id = Column(Integer, primary_key=True)

    car_id = Column(Integer, ForeignKey(Car.id), nullable=False)
    car = relationship('Car', back_populates='trips')

    remaining_seats = Column(SmallInteger, nullable=True)
    start_datetime = Column(DateTime, nullable=False)
    direction = Column(String(31), nullable=False)
    cost = Column(DECIMAL(9, 2), nullable=True)
    is_removed = Column(Boolean, nullable=False, default=False)

    purchases = relationship('Purchase', back_populates='trip')

    def __str__(self):
        return f'{self.start_datetime} {self.direction} trip by {self.car}'


class Station(Base):
    __tablename__ = 'mogiminsk_station'

    id = Column(Integer, primary_key=True)

    provider_id = Column(Integer, ForeignKey(Provider.id), nullable=False)
    provider = relationship('Provider', back_populates='stations')

    name = Column(String(127), nullable=False)
    direction = Column(String(31), nullable=False)
    identifier = Column(String(127), nullable=False)
    order = Column(SmallInteger, nullable=True)
    is_removed = Column(Boolean, nullable=False, default=False)

    purchases = relationship('Purchase', back_populates='station')

    __mapper_args__ = {
        "order_by": order
    }


class Purchase(Base):
    __tablename__ = 'mogiminsk_purchase'

    id = Column(Integer, primary_key=True)

    trip_id = Column(Integer, ForeignKey(Trip.id), nullable=False)
    trip = relationship('Trip', back_populates='purchases')

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', back_populates='purchases')

    station_id = Column(Integer, ForeignKey(Station.id), nullable=True)
    station = relationship('Station', back_populates='purchases')

    seats = Column(SmallInteger, nullable=False, default=1)
    notes = Column(String(255), nullable=True)

    def __str__(self):
        if not self.id:
            return 'Draft purchase.'

        return 'Purchase for {provider}, {direction}, {start_datetime}.' \
               ' {username} ({phone}).'.format(**{
                'provider': self.trip.car.provider.name,
                'direction': self.trip.direction,
                'start_datetime': self.trip.start_datetime,
                'username': self.user.first_name,
                'phone': self.user.phone,
            })


class Conversation(Base):
    __tablename__ = 'mogiminsk_conversation'
    __mapper_args__ = {
        'order_by': 'created_at',
    }

    MESSENGER_TELEGRAM = 'telegram'

    id = Column(Integer, primary_key=True)

    text = Column(Text, nullable=True)
    is_user_message = Column(Boolean, nullable=False)
    seen = Column(Boolean, nullable=False, default=False)
    messenger = Column(String(31), nullable=False)
    context = Column(JSON, default={})

    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    user = relationship('User', back_populates='conversation')

    def __str__(self):
        return self.text

import sys

from sqlalchemy import Column, Integer, String, ForeignKey, \
    JSON, SmallInteger, DateTime, UniqueConstraint, Interval, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func

from mogiminsk.settings import DB_CONNECTION


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
    language = Column(String(5), nullable=True)
    telegram_context = Column(JSON, default='{}')
    telegram_id = Column(Integer, nullable=False, unique=True)


class Provider(Base):
    __tablename__ = 'mogiminsk_provider'
    id = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)
    identifier = Column(String(15), nullable=False, unique=True)

    cars = relationship('Car', back_populates='provider')


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

    def __str__(self):
        return f'{self.start_datetime} {self.direction} trip by {self.car}'

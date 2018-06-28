from enum import Enum
from typing import TypeVar, Type

C = TypeVar('C')


class OptionalObjectFactoryMixin:
    @classmethod
    def create(cls: Type[C], data) -> C:
        if data is None:
            return

        return cls(data)


class Messager(Enum):
    TELEGRAM = 'tg'
    VIBER = 'viber'

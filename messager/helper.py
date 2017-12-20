from typing import TypeVar, Type

C = TypeVar('C')

class OptionalObjectFactoryMixin:
    @classmethod
    def create(cls: Type[C], data) -> C:
        if data is None:
            return

        return cls(data)
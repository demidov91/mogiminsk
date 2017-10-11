from typing import TypeVar, Type

from mogiminsk.utils import get_db

C = TypeVar


class BaseService:
    model = None    # type: Type[C]
    _db = None

    def __init__(self, instance: C):
        self.instance = instance

    def db(self):
        if not self._db:
            self._db = get_db()

        return self._db

    @classmethod
    def query(cls):
        return get_db().query(cls.model)

    @classmethod
    def delete(cls, **kwargs):
        cls.query().filter(**kwargs).delete()

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def id_list(cls, ids):
        return cls.query().filter(cls.model.id.in_(ids))

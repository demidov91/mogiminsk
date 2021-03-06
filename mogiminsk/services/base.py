from typing import TypeVar, Type

from mogiminsk.utils import get_db

M = TypeVar('M')
S = TypeVar('S', bound='BaseService')


class BaseService:
    model = None    # type: Type[M]
    _db = None

    def __init__(self: S, instance: M):
        self.instance = instance

    def db(self):
        if not self._db:
            self._db = get_db()

        return self._db

    @classmethod
    def query(cls):
        return get_db().query(cls.model)

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query().filter_by(**kwargs)

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.query().filter(*args, **kwargs)

    @classmethod
    def delete(cls, **kwargs):
        cls.query().filter(**kwargs).delete()

    @classmethod
    def get(cls: Type[S], id) ->M:
        return cls.query().get(id)

    @classmethod
    def get_service(cls: Type[S], id) ->S:
        return cls(cls.get(id))

    @classmethod
    def id_list(cls, ids):
        return cls.query().filter(cls.model.id.in_(ids))

    @classmethod
    def add(cls, **kwargs):
        instance = cls.model(**kwargs)
        get_db().add(instance)
        return instance

    @property
    def id(self):
        return self.instance.id

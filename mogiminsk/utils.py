from functools import partial
import logging
import json
import pkgutil
from importlib import import_module

from aiohttp import ClientSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from tasklocal import local

from aiohttp_translation import LazyAwareJsonEncoder
from mogiminsk.settings import DB_CONNECTION
from mogiminsk.models import Base as MainBase
from block_ip.models import Base as BlockedIpBase


logger = logging.getLogger(__name__)
_LOCAL = local()

lazy_string_aware_json_dumps = partial(json.dumps, cls=LazyAwareJsonEncoder)


def init_client(app):
    app['client'] = ClientSession(json_serialize=lazy_string_aware_json_dumps)


def destroy_client(app):
    app['client'].close()


def create_db():
    MainBase.metadata.create_all(bind=Session.kw['bind'])
    BlockedIpBase.metadata.create_all(bind=Session.kw['bind'])


def get_db_engine(config):
    return create_engine(URL(**config))


def configure_session():
    Session.configure(bind=get_db_engine(DB_CONNECTION))


def load_sub_modules(module):
    """
    Loads all package submodules.
    """
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        if '.' in name:
            continue

        import_module(f'{module.__name__}.{name}')


def get_db():
    try:
        return _LOCAL.db
    except AttributeError:
        logger.info('Using threaded db session.')
        return threaded_session()


def set_db(db):
    _LOCAL.db = db


def clear_local_data():
    _LOCAL.clear()


Session = sessionmaker()
threaded_session = scoped_session(Session)
configure_session()

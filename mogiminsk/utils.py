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
from viberbot import Api, BotConfiguration

from aiohttp_translation import LazyAwareJsonEncoder
from mogiminsk.settings import DB_CONNECTION, VIBER_TOKEN
from mogiminsk.models import Base as MainBase
from mogiminsk.middleware.block_ip_models import Base as BlockedIpBase


logger = logging.getLogger(__name__)
_LOCAL = local()


def init_client(app):
    app['client'] = ClientSession(json_serialize=partial(json.dumps, cls=LazyAwareJsonEncoder))


def destroy_client(app):
    app['client'].close()


def init_viber_client(app):
    app['viber'] = Api(BotConfiguration(
        name='helloworld',
        auth_token=VIBER_TOKEN,
        avatar=None,
    ))


def destroy_viber_client(app):
    """
    Close client session when it is written in aiohttp.
    """
    pass


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

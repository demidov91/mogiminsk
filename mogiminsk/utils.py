import pkgutil
from importlib import import_module

from aiohttp import ClientSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from tasklocal import local

from mogiminsk.settings import DB_CONNECTION
from mogiminsk.models import Base as MainBase
from mogiminsk.middleware.block_ip_models import Base as BlockedIpBase


_LOCAL = local()


def init_client(app):
    app['client'] = ClientSession()


def destroy_client(app):
    app['client'].close()


def init_db(app):
    MainBase.metadata.create_all(bind=Session.kw['bind'])
    BlockedIpBase.metadata.create_all(bind=Session.kw['bind'])


def close_db(app):
    pass


def get_db_engine(config):
    return create_engine(URL(**config), echo=True)


def configure_session():
    Session.configure(bind=get_db_engine(DB_CONNECTION))


def load_sub_modules(module):
    """
    Loads all package submodules.
    """
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        import_module(f'{module.__name__}.{name}')


def get_db():
    return _LOCAL.db


def set_db(db):
    _LOCAL.db = db


Session = sessionmaker()
threaded_session = scoped_session(Session)
configure_session()

from aiohttp import ClientSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

from mogiminsk.settings import DB_CONNECTION
from mogiminsk.models import Base


def init_client(app):
    app['client'] = ClientSession()


def destroy_client(app):
    app['client'].close()


def init_db(app):
    app['db_engine'] = get_db_engine(DB_CONNECTION)
    Session.configure(bind=app['db_engine'])
    Base.metadata.create_all(app['db_engine'])


def close_db(app):
    app['db_engine'].close()


def get_db_engine(config):
    return create_engine(URL(**config), echo=True)


Session = sessionmaker()
threaded_session = scoped_session(Session)

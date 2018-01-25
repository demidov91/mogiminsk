import logging.config

from block_ip.models import Base as BlockIpBase
from mogiminsk.settings import DB_CONNECTION, LOGGING
from mogiminsk.utils import get_db_engine, Session
from mogiminsk.models import Base


def pytest_configure(config):
    """
    Turn off logging, recreate database and configure *util.Session*
    """
    LOGGING['loggers']['']['level'] = logging.CRITICAL
    logging.config.dictConfig(LOGGING)

    db_connection = DB_CONNECTION.copy()
    db_connection['database'] = 'test_' + db_connection['database']
    engine = get_db_engine(db_connection)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    BlockIpBase.metadata.drop_all(engine)
    BlockIpBase.metadata.create_all(engine)
    Session.configure(bind=engine)

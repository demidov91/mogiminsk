import sys
from mogiminsk.settings import DB_CONNECTION
from mogiminsk.utils import get_db_engine, Session
from mogiminsk.models import Base


def pytest_configure(config):
    """
    Recreate database and configure *util.Session*
    """
    db_connection = DB_CONNECTION.copy()
    db_connection['database'] = 'test_' + db_connection['database']
    engine = get_db_engine(db_connection)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

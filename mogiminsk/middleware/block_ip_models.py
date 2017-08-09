from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


Base = declarative_base()


class BlockedIp(Base):
    __tablename__ = 'middleware_blocked_ip'

    ip = Column(String(31), primary_key=True)
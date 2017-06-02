# coding: utf-8

import datetime
from sqlalchemy import Column, VARCHAR, INTEGER, BINARY, TIMESTAMP, BIGINT
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf.config import Market_CONFIG
from AndroidCrawler.db.sqlutil import ISqlHelper

Base = declarative_base()


class Market_Hiapk(Base):
    """class for mysql db table: Market_Hiapk"""

    __tablename__ = Market_CONFIG.get('Market_Hiapk').get('db_name', 'Market_Hiapk')
    Distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('package_name', VARCHAR(256), nullable=True, index=True, default=None)
    version_code = Column('version_code', VARCHAR(64), nullable=True, index=True, default=None)
    file_name = Column('file_name', VARCHAR(200), nullable=True, default=None)
    date_size = Column('data_size', VARCHAR(64), nullable=True, default=None)
    download_url = Column('download_url', VARCHAR(2048), nullable=True, default=None)
    header = Column('header', VARCHAR(2048), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    Appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    Sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item['package_name'], version_code=item['version_code'],
                   download_url=item['download_url'])


class SqlHelper(ISqlHelper):
    """sql helper for Market_Hiapk"""

    def __init__(self, engine):
        self.table_name = Market_CONFIG.get('Market_Hiapk').get('db_name', 'Market_Hiapk')
        super(SqlHelper, self).__init__(engine)

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_flag(self, row):
        query = self.session.query(Market_Hiapk.download_flag, Market_Hiapk.collect_time).\
            filter(Market_Hiapk.package_name == row.package_name).\
            filter(Market_Hiapk.version_code == row.version_code).\
            order_by(Market_Hiapk.Distributed_id.desc())
        return query.first()

    def query_distributed_id(self, row):
        query = self.session.query(Market_Hiapk.Distributed_id). \
            filter(Market_Hiapk.package_name == row.package_name). \
            filter(Market_Hiapk.version_code == row.version_code). \
            order_by(Market_Hiapk.Distributed_id.desc())
        return query.first()

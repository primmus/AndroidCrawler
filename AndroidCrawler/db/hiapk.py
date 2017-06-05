# coding: utf-8

import datetime
from sqlalchemy import Column, VARCHAR, INTEGER, BINARY, TIMESTAMP, BIGINT
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper

_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class TableHiApk(_Base):
    """class for mysql db table: Market_Hiapk"""

    __tablename__ = _Market_CONFIG.get('Market_Hiapk').get('db_name', 'Market_Hiapk')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('package_name', VARCHAR(256), nullable=True, index=True, default=None)
    version_code = Column('version_code', VARCHAR(64), nullable=True, index=True, default=None)
    file_name = Column('file_name', VARCHAR(200), nullable=True, default=None)
    date_size = Column('data_size', VARCHAR(64), nullable=True, default=None)
    download_url = Column('download_url', VARCHAR(2048), nullable=True, default=None)
    header = Column('header', VARCHAR(2048), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item['package_name'], version_code=item['version_code'],
                   download_url=item['download_url'])


class SqlHiApk(ISqlHelper):
    """sql helper for Market_Hiapk"""

    table_name = _Market_CONFIG.get('Market_Hiapk').get('db_name', 'Market_Hiapk')

    def __init__(self):
        super(SqlHiApk, self).__init__()

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_status(self, row):
        query = self.session.query(TableHiApk.download_flag, TableHiApk.collect_time, TableHiApk.distributed_id).\
            filter(TableHiApk.package_name == row.package_name).\
            filter(TableHiApk.version_code == row.version_code).\
            order_by(TableHiApk.distributed_id.desc())
        download_status = query.first()
        if download_status is None:
            return -1, None, None
        else:
            return download_status

    def query_distributed_id(self, row):
        query = self.session.query(TableHiApk.distributed_id). \
            filter(TableHiApk.package_name == row.package_name). \
            filter(TableHiApk.version_code == row.version_code). \
            order_by(TableHiApk.distributed_id.desc())
        return query.first()

    def item_to_row(self, item):
        return TableHiApk.transform(item)

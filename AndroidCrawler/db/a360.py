# coding: utf-8

import datetime
from sqlalchemy import Column, VARCHAR, INTEGER, BINARY, TIMESTAMP, BIGINT
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper
from sqlalchemy import distinct

_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class Table360(_Base):
    """class for mysql db table: Market_360"""

    __tablename__ = _Market_CONFIG.get('Market_360').get('db_name', 'Market_360')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('PackageName', VARCHAR(256), nullable=False, index=True, default=None)
    version_code = Column('VersionCode', VARCHAR(64), nullable=False, index=True, default=None)
    product_id = Column('ProductID', VARCHAR(32), nullable=True, default=None)
    download_url = Column('download_url', VARCHAR(2048), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item.get('package_name'), version_code=item['version_code'],
                   download_url=item['download_url'], product_id=item.get('product_id', None))


class Sql360(ISqlHelper):
    """sql helper for Market_360"""

    table_name = _Market_CONFIG.get('Market_360').get('table_name', 'Market_360')

    def __init__(self):
        super(Sql360, self).__init__(self.table_name)

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_status(self, row):
        query = self.session.query(Table360.download_flag, Table360.collect_time, Table360.distributed_id). \
            filter(Table360.package_name == row.package_name). \
            filter(Table360.version_code == row.version_code). \
            order_by(Table360.distributed_id.desc())
        download_status = query.first()
        if download_status is None:
            return -1, None, None
        else:
            return download_status

    def query_distributed_id(self, row):
        query = self.session.query(Table360.distributed_id). \
            filter(Table360.package_name == row.package_name). \
            filter(Table360.version_code == row.version_code). \
            order_by(Table360.distributed_id.desc())
        return query.first()

    def query_pkgs(self, offset=0, limit=0):
        if not limit or limit <= 0:
            # query = self.session.query(Table360.package_name, Table360.product_id).\
            #     filter(Table360.package_name.isnot(None)).filter(Table360.product_id.isnot(None)).\
            #     group_by(Table360.package_name, Table360.product_id)
            query = self.session.query(distinct(Table360.product_id)).filter(Table360.product_id.isnot(None))
        else:
            query = self.session.query(distinct(Table360.product_id)).filter(Table360.product_id.isnot(None))\
                .limit(limit).offset(offset)
        pkgs = query.all()
        return [pkg[0] for pkg in pkgs if pkg and pkg[0]]

    def item_to_row(self, item):
        return Table360.transform(item)

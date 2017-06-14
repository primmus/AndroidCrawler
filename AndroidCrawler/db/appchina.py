# coding: utf-8


from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper
from AndroidCrawler.db.base import TableAppChina


_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class SqlAppChina(ISqlHelper):
    """sql helper for Market_Appchina"""

    table_name = _Market_CONFIG.get('Market_Appchina').get('table_name', 'Market_Appchina')

    def __init__(self):
        super(SqlAppChina, self).__init__(self.table_name)

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_status(self, row):
        query = self.session.query(TableAppChina.download_flag, TableAppChina.collect_time, TableAppChina.distributed_id). \
            filter(TableAppChina.package_name == row.package_name). \
            filter(TableAppChina.version_code == row.version_code). \
            order_by(TableAppChina.distributed_id.desc())
        download_status = query.first()
        if download_status is None:
            return -1, None, None
        else:
            return download_status

    def query_distributed_id(self, row):
        query = self.session.query(TableAppChina.distributed_id). \
            filter(TableAppChina.package_name == row.package_name). \
            filter(TableAppChina.version_code == row.version_code). \
            order_by(TableAppChina.distributed_id.desc())
        return query.first()

    def query_pkgs(self, offset=0, limit=0):
        if not limit or limit <= 0:
            query = self.session.query(distinct(TableAppChina.package_name)).\
                filter(TableAppChina.package_name.isnot(None))
        else:
            query = self.session.query(distinct(TableAppChina.package_name)).\
                filter(TableAppChina.package_name.isnot(None)).limit(limit).offset(offset)
        pkgs = query.all()
        return [pkg[0] for pkg in pkgs if pkg and pkg[0]]

    def item_to_row(self, item):
        return TableAppChina.transform(item)

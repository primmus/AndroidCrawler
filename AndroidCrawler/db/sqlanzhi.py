# coding: utf-8

from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper
from AndroidCrawler.db.base import TableAnZhi as Table

_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class SqlAnZhi(ISqlHelper):
    """sql helper for Market_Anzhi"""

    table_name = _Market_CONFIG.get('Market_Anzhi').get('table_name', 'Market_Anzhi')

    def __init__(self):
        super(SqlAnZhi, self).__init__(self.table_name)

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_status(self, row):
        query = self.session.query(Table.download_flag, Table.collect_time, Table.distributed_id).\
            filter(Table.package_name == row.package_name).\
            filter(Table.version_code == row.version_code).\
            order_by(Table.distributed_id.desc())
        download_status = query.first()
        if download_status is None:
            return -1, None, None
        else:
            return download_status

    def query_distributed_id(self, row):
        query = self.session.query(Table.distributed_id). \
            filter(Table.package_name == row.package_name). \
            filter(Table.version_code == row.version_code). \
            order_by(Table.distributed_id.desc())
        return query.first()

    def query_pkgs(self, offset=0, limit=0):
        if not limit or limit <= 0:
            query = self.session.query(distinct(Table.package_name)).filter(Table.package_name.isnot(None))
        else:
            query = self.session.query(distinct(Table.package_name)).\
                filter(Table.package_name.isnot(None)).limit(limit).offset(offset)
        for pkg in query.all():
            yield pkg

    def item_to_row(self, item):
        return Table.transform(item)

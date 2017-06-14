# coding: utf-8

from sqlalchemy import distinct
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper
from AndroidCrawler.db.base import Table360

_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


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

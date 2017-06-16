# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config
from AndroidCrawler.db.sqlutil import ISqlHelper
from AndroidCrawler.db.base import TableMuMaYi

_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class SqlMuMaYi(ISqlHelper):
    """sql helper for Market_MuMaYi"""

    table_name = _Market_CONFIG.get('Market_Mumayi').get('table_name', 'Market_Mumayi')

    def __init__(self):
        super(SqlMuMaYi, self).__init__(self.table_name)

    def init_db(self):
        pass

    def drop_db(self):
        pass

    def query_download_status(self, row):
        query = self.session.query(TableMuMaYi.download_flag, TableMuMaYi.collect_time, TableMuMaYi.distributed_id). \
            filter(TableMuMaYi.package_name == row.package_name). \
            filter(TableMuMaYi.version_code == row.version_code). \
            order_by(TableMuMaYi.distributed_id.desc())
        download_status = query.first()
        if download_status is None:
            return -1, None, None
        else:
            return download_status

    def query_distributed_id(self, row):
        query = self.session.query(TableMuMaYi.distributed_id). \
            filter(TableMuMaYi.package_name == row.package_name). \
            filter(TableMuMaYi.version_code == row.version_code). \
            order_by(TableMuMaYi.distributed_id.desc())
        return query.first()

    def query_pkgs(self, offset=0, limit=0):
        if not limit or limit <= 0:
            query = self.session.query(TableMuMaYi.package_name, TableMuMaYi.app_id)\
                .filter(TableMuMaYi.package_name.isnot(None))\
                .filter(TableMuMaYi.app_id.isnot(None))\
                .group_by(TableMuMaYi.package_name, TableMuMaYi.app_id)
        else:
            query = self.session.query(TableMuMaYi.package_name, TableMuMaYi.app_id)\
                .filter(TableMuMaYi.package_name.isnot(None))\
                .filter(TableMuMaYi.app_id.isnot(None))\
                .group_by(TableMuMaYi.package_name, TableMuMaYi.app_id)\
                .limit(limit).offset(offset)
        for pkg_and_app_id in query.all():
            yield pkg_and_app_id

    def item_to_row(self, item):
        return TableMuMaYi.transform(item)

# coding: utf-8

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from AndroidCrawler.conf.config import DB_CONFIG
from AndroidCrawler.db.base import DisCrawlerTasks
from AndroidCrawler.db.base import IPProxyPool
# from AndroidCrawler.db.hiapk import SqlHiApk


class ISqlHelper(object):
    """interface for sql helper"""
    table_name = None
    # market = None

    def __init__(self, table_name=None):
        if table_name is not None:
            self.table_name = table_name
        elif not getattr(self, 'table_name', None):
            raise ValueError("%s must have a table name" % type(self).__name__)

        # if market is not None:
        #     self.market = market
        # elif not getattr(self, 'market', None):
        #     raise ValueError("%s must have a market name" % type(self).__name__)

        engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'], echo=True)
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def query_download_status(self, row):
        raise NotImplemented

    def query_distributed_id(self, row):
        raise NotImplemented

    def query_proxy_by_validator(self, validator):
        query = self.session.query(IPProxyPool).filter(IPProxyPool.validator == validator).\
            filter(IPProxyPool.vali_count > 0)
        return [(proxy.ip, proxy.port) for proxy in query.all() if proxy is not None]

    def query_pkgs(self, offset=0, limit=0):
        raise NotImplemented

    def add(self, row):
        self.session.add(row)
        self.session.commit()

    def add_to_dis_crawler_tasks(self, row):
        dis_row = DisCrawlerTasks(submitter=self.table_name, url=row.download_url,
                                  id=row.distributed_id, create_time=datetime.datetime.utcnow())
        self.session.add(dis_row)
        self.session.commit()

    def item_to_row(self, item):
        raise NotImplemented

# class SqlUtil(object):
#
#     engine = None
#     session = None
#     sql_helper = {}
#
#     def __init__(self):
#         self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'], echo=True)
#         session_cls = sessionmaker(bind=self.engine)
#         self.session = session_cls()
#         self.sql_helper[SqlHiApk.market] = SqlHiApk(self.engine, self.session)
#
#     def get_sql_helper(self, market):
#         return self.sql_helper.get(market, None)




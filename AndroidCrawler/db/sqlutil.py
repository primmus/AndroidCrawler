# coding: utf-8

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from AndroidCrawler.conf.config import DB_CONFIG
from AndroidCrawler.db.base import DisCrawlerTasks


class ISqlHelper(object):
    """interface for sql helper"""

    table_name = None

    def __init__(self, table_name=None):
        if table_name is not None:
            self.table_name = table_name
        elif not getattr(self, 'table_name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
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
#     def __init__(self):
#         engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'], echo=True)
#         sql_helper = {}
#         for market_key, info in DB_CONFIG.items():
#             table_name = info.get('table_name'),
#             sql_helper_cls = info.get('sql_helper')
#             sql_helper = sql_helper_cls()
#
#         pass


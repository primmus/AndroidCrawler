# coding: utf-8

import datetime

from sqlalchemy import Column, VARCHAR, INTEGER, BINARY, TIMESTAMP, BIGINT
from sqlalchemy.orm import sessionmaker

from AndroidCrawler.AndroidCrawler.db.base import Base
from AndroidCrawler.AndroidCrawler.db.base import engine
from AndroidCrawler.AndroidCrawler.db.base import DisCrawlerTasks
from AndroidCrawler.AndroidCrawler.conf.config import Market_CONFIG


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


class SqlHelper(object):

    def __init__(self):
        self.table_name = Market_CONFIG.get('Market_Hiapk').get('db_name', 'Market_Hiapk')
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

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

    def add(self, row):
        self.session.add(row)
        self.session.commit()

    def add_to_dis_crawler_tasks(self, row):
        dis_row = DisCrawlerTasks(submitter=self.table_name, url=row.download_url,
                                  id=row.Distributed_id, create_time=datetime.datetime.utcnow())
        self.session.add(dis_row)
        self.session.commit()

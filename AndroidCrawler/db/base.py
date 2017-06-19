# coding: utf-8

import datetime
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER, BINARY, TIMESTAMP, SMALLINT, BIGINT, FLOAT
from sqlalchemy.ext.declarative import declarative_base

from AndroidCrawler.conf import config


_Base = declarative_base()
_Market_CONFIG = config.MARKET_CONFIG


class DisCrawlerTasks(_Base):
    """class for mysql db table DisCrawlerTasks """
    __tablename__ = 'DisCrawlerTasks'
    submitter = Column('submitter', VARCHAR(128), nullable=True, default=None, index=True)
    url = Column('url', TEXT, nullable=False, default=None)
    header = Column('header', TEXT, nullable=True, default=None)
    priority = Column('priority', INTEGER, nullable=True, default=4)
    app_sha1 = Column('app_sha1', BINARY(20), nullable=True, default=None, index=True)
    status = Column('status', INTEGER, nullable=True, default=0)
    submit_time = Column('submit_time', TIMESTAMP, nullable=False,
                         default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    create_time = Column('create_time', TIMESTAMP, nullable=True, default=None, index=True)
    status_code = Column('status_code', INTEGER, nullable=True, default=0)
    market_table = Column('table_name', VARCHAR(20), nullable=True, default=None)
    id = Column('id', BIGINT, nullable=True, default=None)
    job_id = Column('job_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    uniqueApk = Column('UniqueApk', SMALLINT, nullable=True, default=0)
    dealTag = Column('dealTag', SMALLINT, nullable=True, default=0)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    mac_address = Column('mac_address', VARCHAR(128), nullable=True, default=None, index=True)
    download_count = Column('download_count', INTEGER, nullable=False, default=0, index=True)
    upload_flag = Column('upload_flag', INTEGER, nullable=True, default=0)
    sha256 = Column('Sha256', BINARY(32), nullable=True, default=None, index=True)


class IPProxyPool(_Base):
    """class for mysql db table IPProxyPool """
    __tablename__ = 'IPProxyPool'
    id = Column('id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    ip = Column('ip', VARCHAR(25), nullable=False)
    port = Column('port', INTEGER, nullable=False)
    validator = Column('validator', VARCHAR(64), nullable=True)
    country = Column('country', TEXT, nullable=True, default=None)
    anonymity = Column('anonymity', SMALLINT, nullable=True, default=None)
    https = Column('https', VARCHAR(4), nullable=True, default=None)
    speed = Column('speed', FLOAT, nullable=True, default=None)
    source = Column('source', VARCHAR(20), nullable=True, default=None)
    save_time = Column('save_time', TIMESTAMP, nullable=False,
                       default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    vali_count = Column('vali_count', INTEGER, nullable=True, default=3)


class Table360(_Base):
    """class for mysql db table: Market_360"""

    __tablename__ = _Market_CONFIG.get('Market_360').get('table_name', 'Market_360')
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


class TableHiApk(_Base):
    """class for mysql db table: Market_Hiapk"""

    __tablename__ = _Market_CONFIG.get('Market_Hiapk').get('table_name', 'Market_Hiapk')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('package_name', VARCHAR(256), nullable=True, index=True, default=None)
    version_code = Column('version_code', VARCHAR(64), nullable=True, index=True, default=None)
    file_name = Column('file_name', VARCHAR(200), nullable=True, default=None)
    data_size = Column('data_size', VARCHAR(64), nullable=True, default=None)
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


class TableMuMaYi(_Base):
    """class for mysql db table: Market_Mumayi"""

    __tablename__ = _Market_CONFIG.get('Market_Mumayi').get('table_name', 'Market_Mumayi')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    app_id = Column('ApplicationId', VARCHAR(128), nullable=True, index=True, default=None)
    package_name = Column('PackageName', VARCHAR(256), nullable=False, index=True, default=None)
    version_code = Column('ApplicationVersionCode', VARCHAR(64), nullable=False, index=True, default=None)
    app_name = Column('ApplicationName', VARCHAR(64), nullable=True, default=None)
    download_url = Column('download_url', VARCHAR(2048), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item['package_name'], version_code=item['version_code'],
                   download_url=item['download_url'], app_id=item.get('app_id', None),
                   app_name=item.get('app_name', None))


class TableAppChina(_Base):
    """class for mysql db table: Market_Appchina"""

    __tablename__ = _Market_CONFIG.get('Market_Appchina').get('table_name', 'Market_Appchina')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('package_name', VARCHAR(256), nullable=True, index=True, default=None)
    version_code = Column('version_code', INTEGER, nullable=True, index=True, default=None)
    product_id = Column('product_id', VARCHAR(256), nullable=True, default=None)
    data_size = Column('size', BIGINT, nullable=True, default=None)
    category = Column('category', TEXT, nullable=True, default=None)
    download_url = Column('download_url', VARCHAR(1024), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item['package_name'], version_code=item['version_code'],
                   download_url=item['download_url'], product_id=item['product_id'])


class TableAnZhi(_Base):
    """class for mysql db table: Market_Anzhi"""

    __tablename__ = _Market_CONFIG.get('Market_Anzhi').get('table_name', 'Market_Anzhi')
    distributed_id = Column('Distributed_id', BIGINT, nullable=False, autoincrement=True, primary_key=True)
    package_name = Column('PackageName', VARCHAR(128), nullable=False, index=True, default=None)
    version_code = Column('ApplicationVersionCode', VARCHAR(64), nullable=True, index=True, default=None)
    app_id = Column('ApplicationId', VARCHAR(128), nullable=True, index=True, default=None)
    download_url = Column('download_url', VARCHAR(1024), nullable=True, default=None)
    download_flag = Column('download_flag', INTEGER, nullable=True, default=0)
    collect_time = Column('collect_time', TIMESTAMP, nullable=False,
                          default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    appsha1 = Column('Appsha1', VARCHAR(45), nullable=True, index=True, default=None)
    sha256 = Column('Sha256', BINARY(32), nullable=True, index=True, default=None)

    @classmethod
    def transform(cls, item):
        return cls(package_name=item['package_name'], version_code=item['version_code'],
                   download_url=item['download_url'], app_id=item['app_id'])

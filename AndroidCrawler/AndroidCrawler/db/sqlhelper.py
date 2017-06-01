# coding: utf-8

# import sqlalchemy
import datetime
from sqlalchemy import create_engine, Column, VARCHAR, TEXT, INTEGER, BINARY, TIMESTAMP, BIGINT
from sqlalchemy import SMALLINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DisCrawlerTasks(Base):
    """ """
    __table_name__ = None
    submitter = Column(VARCHAR(128), nullable=True, default=None)
    url = Column(TEXT, nullable=False)
    header = Column(TEXT, nullable=True, default=None)
    priority = Column(INTEGER(11), nullable=True, default=4)
    app_sha1 = Column(BINARY(20), nullable=True, default=None)
    status = Column(INTEGER(11), nullable=True, default=0)
    submit_time = Column(TIMESTAMP, nullable=False, default=None, onupdate=datetime.datetime.utcnow)  #
    create_time = Column(TIMESTAMP, nullable=True, default=None)
    status_code = Column(INTEGER(11), nullable=False, default=0)
    table_name = Column(VARCHAR(20), nullable=True, default=None)
    id = Column(BIGINT(20), nullable=True, default=None)
    job_id = Column(BIGINT(20), nullable=False, autoincrement=True, primary_key=True)
    UniqueApk = Column(SMALLINT(1), nullable=True, default=0)
    dealTag = Column(SMALLINT(1), nullable=True, default=0)
    download_flag = Column(INTEGER(11), nullable=True, default=0)
    mac_address = Column(VARCHAR(128), nullable=True, default=None)
    download_count = Column(INTEGER(11), nullable=False, default=0)
    upload_flag = Column(INTEGER(11), nullable=True, default=0)
    Sha256 = Column(BINARY(32), nullable=True, default=None)

    def __init__(self, table_name):
        self.__table_name__ = table_name

"""
Create Table

CREATE TABLE `DisCrawlerTasks` (
  `submitter` varchar(128) CHARACTER SET latin1 DEFAULT NULL,
  `url` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `header` text CHARACTER SET utf8 COLLATE utf8_bin,
  `priority` int(11) DEFAULT '4',
  `app_sha1` binary(20) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  `submit_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `create_time` timestamp NULL DEFAULT NULL,
  `status_code` int(11) DEFAULT '0',
  `table_name` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `id` bigint(20) DEFAULT NULL,
  `job_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `UniqueApk` tinyint(1) DEFAULT '0',
  `dealTag` tinyint(1) DEFAULT '0',
  `download_flag` int(11) DEFAULT '0',
  `mac_address` varchar(128) CHARACTER SET latin1 DEFAULT NULL,
  `download_count` int(11) NOT NULL DEFAULT '0',
  `upload_flag` int(11) DEFAULT '0',
  `Sha256` binary(32) DEFAULT NULL,
  PRIMARY KEY (`job_id`),
  KEY `queryIndex` (`submitter`,`id`),
  KEY `getTaskIndex` (`status`),
  KEY `index_count` (`download_count`),
  KEY `index_mac` (`mac_address`),
  KEY `app_sha1` (`app_sha1`),
  KEY `NewIndex1` (`create_time`),
  KEY `Sha256` (`Sha256`),
  KEY `submitter` (`submitter`,`id`)
) ENGINE=InnoDB AUTO_INCREMENT=195488893 DEFAULT CHARSET=utf8
"""

class SqlHelper(object):
    pass
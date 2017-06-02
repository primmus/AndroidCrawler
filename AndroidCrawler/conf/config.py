# coding: utf-8

import logging

LOG_CONFIG = {
    'LOG_DIR': 'log/',
    'LOG_FILE_SIZE': 10*1024*1024,
    'LOG_FILE_BACKUP_COUNT': 3,
    'LOG_LEVER': logging.DEBUG,
    'LOG_FORMAT': logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')
}

DB_CONFIG = {
    'DB_CONNECT_TYPE': 'sqlalchemy',
    'DB_CONNECT_STRING': 'mysql+mysqldb://root:@10.64.202.37/UniCrawler?charset=utf8'
}

Market_CONFIG = {
    'Market_Hiapk': {
        'db_name': 'Market_Hiapk',
    },
    'Market_360': {
        'db_name': 'Market_360',
    }
}








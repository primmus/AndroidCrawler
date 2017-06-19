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
    'DB_CONNECT_STRING': 'mysql+pymysql://admin:mac8.6@10.64.202.37/UniCrawler?charset=utf8'
}


MARKET_CONFIG = {
    'Market_Hiapk': {
        'table_name': 'Market_Hiapk',
        'validator': 'Market_Hiapk'
    },
    'Market_360': {
        'table_name': 'Market_360',
        'validator': 'Market_360'
    },
    'Market_Appchina': {
        'table_name': 'Market_Appchina',
        'validator': 'Market_Appchina'
    },
    'Market_Mumayi': {
        'table_name': 'Market_Mumayi',
        'validator': 'Market_Mumayi'
    },
    'Market_Anzhi': {
        'table_name': 'Market_Anzhi',
        'validator': 'Market_Anzhi'
    }
}








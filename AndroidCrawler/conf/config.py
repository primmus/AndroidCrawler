# coding: utf-8

import logging
# from AndroidCrawler.db.hiapk import SqlHiApk
# from AndroidCrawler.spiders.hiapk import CategorySpider as HiApkCategorySpider, NewSpider as HiApkNewSpider


LOG_CONFIG = {
    'LOG_DIR': 'log/',
    'LOG_FILE_SIZE': 10*1024*1024,
    'LOG_FILE_BACKUP_COUNT': 3,
    'LOG_LEVER': logging.DEBUG,
    'LOG_FORMAT': logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')
}


DB_CONFIG = {
    'DB_CONNECT_TYPE': 'sqlalchemy',
    'DB_CONNECT_STRING': 'mysql+mysqldb://admin:mac8.6@10.64.202.37/UniCrawler?charset=utf8'
}
MARKET_CONFIG = {
    'Market_Hiapk': {
        'enabled': True,
        'table_name': 'Market_Hiapk',
        # 'sql_helper': SqlHiApk,
        # 'spiders': {
        #     HiApkNewSpider,
        #     HiApkCategorySpider
        # }
    },
    'Market_360': {
        'enabled': False,
        'table_name': 'Market_360',
        # 'sql_helper': None,
        # 'spiders': None
    }
}








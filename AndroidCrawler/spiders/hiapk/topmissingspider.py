# coding = utf-8

import os
import logging
import sys
import time
from logging.handlers import RotatingFileHandler

import scrapy
from AndroidCrawler.items import HiApkItem
# from six.moves.urllib.parse import urljoin
from w3lib.url import safe_url_string

from AndroidCrawler.conf import config
from AndroidCrawler.db.hiapk import SqlHiApk


reload(sys)
sys.setdefaultencoding('utf8')


class TopMissingSpider(scrapy.Spider):
    """top missing spider, crawl top missing apks"""

    name = 'Market_Hiapk.topmissingspider'
    allowed_domains = ['hiapk.com']
    sql_helper = SqlHiApk()

    validator = config.MARKET_CONFIG.get('Market_Hiapk').get('validator', 'Market_Hiapk')
    proxy_pool = []
    proxy_pool_update_time = time.time()
    pkg_pool = []

    def __init__(self, *args, **kwargs):
        super(TopMissingSpider, self).__init__(*args, **kwargs)
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)
        self.pkg_pool = self.sql_helper.query_pkgs()
        self.start_urls = ['http://apk.hiapk.com/appinfo/com.baidu.searchbox']
        # self.get_proxy_pool()

    def __init_logger(self, logger):
        LOG_CONFIG = config.LOG_CONFIG
        log_dir = LOG_CONFIG.get('LOG_DIR', 'log/') + 'hiapk/'
        log_file = log_dir + self.name + '.log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_hander = RotatingFileHandler(log_file, maxBytes=LOG_CONFIG.get('LOG_FILE_SIZE', 10 * 1024 * 1024),
                                         backupCount=LOG_CONFIG.get('LOG_FILE_BACKUP_COUNT', 3))
        log_hander.setLevel(LOG_CONFIG.get('LOG_LEVER', logging.DEBUG))
        log_hander.setFormatter(LOG_CONFIG.get('LOG_FORMAT'))
        logger.addHandler(log_hander)

    @property
    def get_proxy_pool(self):
        if not self.proxy_pool or (time.time() - self.proxy_pool_update_time) > 10 * 60:
            new_proxy_pool = self.sql_helper.query_proxy_by_validator(self.validator)
            if not new_proxy_pool:
                self.proxy_pool = new_proxy_pool
                self.proxy_pool_update_time = time.time()
        else:
            return self.proxy_pool

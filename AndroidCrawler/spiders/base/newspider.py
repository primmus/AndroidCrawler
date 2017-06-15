# coding = utf-8

import os
import logging
import time
import scrapy
from logging.handlers import RotatingFileHandler
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from AndroidCrawler.conf import config


class BaseNewSpider(scrapy.Spider):
    """new spider module"""

    proxy_pool = []
    proxy_pool_update_time = time.time()
    sql_helper = None
    download_delay = 5
    dont_proxy = False

    def __init__(self, name, market, *args, **kwargs):
        super(BaseNewSpider, self).__init__(name=name, *args, **kwargs)
        self.market = market
        self.validator = config.MARKET_CONFIG.get('market').get('validator', None)
        logger = logging.getLogger(self.name)
        self._init_logger(logger)
        # self._init_start_urls()

    def _init_logger(self, logger):
        log_config = config.LOG_CONFIG
        log_dir = log_config.get('LOG_DIR', 'log/') + self.name.split('.')[0] + '/'
        log_file = log_dir + self.name.split('.')[-1] + '.log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_hander = RotatingFileHandler(log_file, maxBytes=log_config.get('LOG_FILE_SIZE', 10*1024*1024),
                                         backupCount=log_config.get('LOG_FILE_BACKUP_COUNT', 3))
        log_hander.setLevel(log_config.get('LOG_LEVER', logging.DEBUG))
        log_hander.setFormatter(log_config.get('LOG_FORMAT'))
        logger.addHandler(log_hander)

    @property
    def get_proxy_pool(self):
        if not self.sql_helper or not self.validator:
            return []
        if not self.proxy_pool or (time.time() - self.proxy_pool_update_time) > 10*60:
            new_proxy_pool = self.sql_helper.query_proxy_by_validator(self.validator)
            if not new_proxy_pool:
                self.proxy_pool = new_proxy_pool
                self.proxy_pool_update_time = time.time()
        else:
            return self.proxy_pool

    def _init_start_urls(self):
        raise NotImplemented

    def parse(self, response):
        raise NotImplemented

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back, priority=0)

    def err_back(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            self.logger.error('TimeoutError on %s', request.url)
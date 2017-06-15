# coding = utf-8

import os
import logging
import scrapy
import time
from logging.handlers import RotatingFileHandler
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.conf import config
from AndroidCrawler.db.a360 import Sql360
from AndroidCrawler.items import A360Item


class UpdateSpider(scrapy.Spider):
    """market 360 update spider, crawl update spider"""

    name = "Market_360.updatespider"
    allow_domains = ['zhushou.360.cn']
    validator = config.MARKET_CONFIG.get('Market_360').get('validator', 'Market_360')
    proxy_pool = []
    proxy_pool_update_time = time.time()
    sql_helper = Sql360()
    download_delay = 30
    dont_proxy = True

    def __init__(self, *args, **kwargs):
        super(UpdateSpider, self).__init__(*args, **kwargs)
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)

    def __init_logger(self, logger):
        log_config = config.LOG_CONFIG
        log_dir = log_config.get('LOG_DIR', 'log/') + 'a360/'
        log_file = log_dir + self.name + '.log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_hander = RotatingFileHandler(log_file, maxBytes=log_config.get('LOG_FILE_SIZE', 10*1024*1024),
                                         backupCount=log_config.get('LOG_FILE_BACKUP_COUNT', 3))
        log_hander.setLevel(log_config.get('LOG_LEVER', logging.DEBUG))
        log_hander.setFormatter(log_config.get('LOG_FORMAT'))
        logger.addHandler(log_hander)

    @property
    def get_proxy_pool(self):
        if not self.proxy_pool or (time.time() - self.proxy_pool_update_time) > 10*60:
            new_proxy_pool = self.sql_helper.query_proxy_by_validator(self.validator)
            if not new_proxy_pool:
                self.proxy_pool = new_proxy_pool
                self.proxy_pool_update_time = time.time()
        else:
            return self.proxy_pool

    def start_requests(self):
        invalid_count, offset, limit = 0, 0, 5000
        while invalid_count < 3:
            pkg_pool = self.sql_helper.query_pkgs(offset=offset*limit, limit=limit)
            offset += 1
            invalid_count = 0 if pkg_pool else invalid_count+1
            if pkg_pool:
                for pkg in pkg_pool:
                    if not pkg or '.apk' in pkg:
                        continue
                    url = 'http://zhushou.360.cn/detail/index/soft_id/{0}'.format(pkg)
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, errback=self.err_back,
                                         meta={'dont_retry': True, 'dont_proxy': self.dont_proxy})

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        hrefs = response.xpath('//a[re:match(@href, "&url=.+\.apk")]/@href').extract()
        for href in hrefs:
            try:
                query = href.replace('zhushou360://', '').strip()
                download_url = urlparse.parse_qs(query).get('url')[0]
                product_id = urlparse.parse_qs(query).get('softid')[0]
                app_md5 = urlparse.parse_qs(query).get('appmd5')[0]

                tag = download_url.split('/')[-1]
                package_name = tag.split('_')[0]
                version_code = tag.split('_')[-1].split('.apk')[0]

                item = A360Item()
                item['package_name'] = package_name
                item['version_code'] = version_code
                item['product_id'] = product_id
                item['app_md5'] = app_md5
                item['download_url'] = download_url

                yield item
            except:
                self.logger.warning('parse download url failed: {0}'.format(href))

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

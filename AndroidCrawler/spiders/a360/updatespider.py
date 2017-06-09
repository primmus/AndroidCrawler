# coding = utf-8

import os
import logging
import sys
import time
from logging.handlers import RotatingFileHandler

import scrapy
import urlparse

from AndroidCrawler.conf import config
from AndroidCrawler.db.a360 import Sql360
from AndroidCrawler.items import A360Item

reload(sys)
sys.setdefaultencoding('utf8')


class UpdateSpider(scrapy.Spider):
    """market 360 update spider, crawl update spider"""

    name = "Market_360.updatespider"
    allow_domains = ['zhushou.360.cn']
    validator = config.MARKET_CONFIG.get('Market_360').get('validator', 'Market_360')
    proxy_pool = []
    proxy_pool_update_time = time.time()
    sql_helper = Sql360()
    pkg_pool = []

    def __init__(self, *args, **kwargs):
        super(UpdateSpider, self).__init__(*args, **kwargs)
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)
        self.pkg_pool = self.sql_helper.query_pkgs(offset=0, limit=5000)
        self.offset = 1
        self.no_pkg_count = 0

        for i in range(0, 5000):
            if self.pkg_pool:
                product_id = self.pkg_pool.pop()
                self.start_urls.append('http://zhushou.360.cn/detail/index/soft_id/{0}'.format(product_id))

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
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

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

        follow = self._get_follow_url()
        if follow:
            yield scrapy.Request(url=follow, callback=self.parse, dont_filter=True)

    def _get_follow_url(self):
        if self.no_pkg_count >= 5:
            return
        if not self.pkg_pool:
            self.pkg_pool = self.sql_helper.query_pkgs(offset=self.offset*5000, limit=5000)
            self.no_pkg_count = 0 if self.pkg_pool else self.no_pkg_count+1
            self.offset = self.offset + 1 if self.pkg_pool else self.offset
        if self.pkg_pool:
            product_id = self.pkg_pool.pop()
            return 'http://zhushou.360.cn/detail/index/soft_id/{0}'.format(product_id)

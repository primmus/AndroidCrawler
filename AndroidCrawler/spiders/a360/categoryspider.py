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


class CategorySpider(scrapy.Spider):
    """market 360 category spider, crawl category apks"""

    name = "Market_360.categoryspider"
    allow_domains = ['zhushou.360.cn']
    categorys = [1, 2, 11, 12, 14, 13, 15, 16, 17, 102228, 102230, 102231, 102232, 102139, 102233,
                 101587, 19, 20, 100451, 51, 52, 53, 54, 102238]
    ranks = ['newest', 'weekdownload', 'download', 'poll']
    validator = config.MARKET_CONFIG.get('Market_360').get('validator', 'Market_360')
    proxy_pool = []
    proxy_pool_update_time = time.time()
    sql_helper = Sql360()
    download_delay = 10

    def __init__(self, *args, **kwargs):
        super(CategorySpider, self).__init__(*args, **kwargs)
        for page in range(1, 101):
            for rank in self.ranks:
                for category in self.categorys:
                    self.start_urls.append('http://zhushou.360.cn/list/index/cid/{0}/order/{1}/?page={2}'.format(category, rank, page))
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
        if not self.proxy_pool or (time.time() - self.proxy_pool_update_time) > 10 * 60:
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






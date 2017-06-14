# coding = utf-8

import os
import logging
import time
from logging.handlers import RotatingFileHandler

import scrapy
from AndroidCrawler.items import HiApkItem
from w3lib.url import safe_url_string

from AndroidCrawler.conf import config
from AndroidCrawler.db.hiapk import SqlHiApk


class UpdateSpider(scrapy.Spider):
    """hiapk update spider, crawl update apks"""

    name = 'Market_Hiapk.updatespider'
    allowed_domains = ['hiapk.com']
    sql_helper = SqlHiApk()

    validator = config.MARKET_CONFIG.get('Market_Hiapk').get('validator', 'Market_Hiapk')
    proxy_pool = []
    proxy_pool_update_time = time.time()

    def __init__(self, *args, **kwargs):
        super(UpdateSpider, self).__init__(*args, **kwargs)
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)

    def __init_logger(self, logger):
        log_config = config.LOG_CONFIG
        log_dir = log_config.get('LOG_DIR', 'log/') + 'hiapk/'
        log_file = log_dir + self.name + '.log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_hander = RotatingFileHandler(log_file, maxBytes=log_config.get('LOG_FILE_SIZE', 10 * 1024 * 1024),
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
        invalid_count, offset, limit = 0, 0, 5000
        while invalid_count < 3:
            pkg_pool = self.sql_helper.query_pkgs(offset=offset, limit=limit)
            offset += 1
            invalid_count = 0 if pkg_pool else invalid_count+1
            for pkg in pkg_pool:
                url = 'http://apk.hiapk.com/appdown/{0}'.format(pkg)
                yield scrapy.Request(url=url, callback=self.parse, method='HEAD', dont_filter=True,
                                     meta={'dont_redirect': True, 'dont_obey_robotstxt': True,
                                           'handle_httpstatus_list': (301, 302, 303, 307),
                                           'dont_retry': True})

    def parse(self, response):
        self.logger.info('current parse_item url: {0}'.format(response.url))

        if 'Location' in response.headers:
            location = safe_url_string(response.headers['location'])
            redirected_url = location
            download_url = redirected_url
            try:
                package_name = download_url.split('/')[-1].split('_')[0]
                version_code = download_url.split('/')[-1].split('_')[-1].split('.')[0]
                item = HiApkItem()
                item['package_name'] = package_name
                item['version_code'] = version_code
                item['download_url'] = download_url
                yield item
            except:
                pass



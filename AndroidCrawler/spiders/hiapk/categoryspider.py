# coding = utf-8

import os
import logging
import time
from logging.handlers import RotatingFileHandler
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

import scrapy
from AndroidCrawler.items import HiApkItem
from w3lib.url import safe_url_string

from AndroidCrawler.conf import config
from AndroidCrawler.db.hiapk import SqlHiApk


class CategorySpider(scrapy.Spider):
    """hiapk category spider, crawl apks by category"""

    name = 'Market_Hiapk.categoryspider'
    market = 'Market_Hiapk'
    allowed_domains = ['hiapk.com']
    sql_helper = SqlHiApk()
    categorys = {'apps', 'apps/MediaAndVideo', 'apps/DailyLife', 'apps/Social', 'apps/Finance',
                 'apps/Tools', 'apps/TravelAndLocal', 'apps/Communication', 'apps/Shopping',
                 'apps/Reading', 'apps/Education', 'apps/NewsAndMagazines', 'apps/HealthAndFitness',
                 'apps/AntiVirus', 'apps/Browser', 'apps/Productivity', 'apps/Personalization',
                 'apps/Input', 'apps/Photography',
                 'games', 'games/OnlineGames', 'games/Casual', 'games/RolePlaying', 'games/BrainAndPuzzle',
                 'games/Shooting', 'games/Sports', 'games/Children', 'games/Chess', 'games/Strategy',
                 'games/Simulation', 'games/Racing'}
    validator = config.MARKET_CONFIG.get('Market_Hiapk').get('validator', 'Market_Hiapk')
    proxy_pool = []
    proxy_pool_update_time = time.time()
    download_delay = 10
    dont_proxy = False

    def __init__(self, *args, **kwargs):
        super(CategorySpider, self).__init__(*args, **kwargs)
        for category in self.categorys:
            for sort in ['5', '8', '9']:
                for page in range(1, 51):
                    url = 'http://apk.hiapk.com/{0}?sort={1}&pi={2}'.format(category, sort, page)
                    self.start_urls.append(url)
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)

    def __init_logger(self, logger):
        log_config = config.LOG_CONFIG
        log_dir = log_config.get('LOG_DIR', 'log/') + 'hiapk/'
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
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': True}, errback=self.err_back)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        referers = response.xpath('//a[re:match(@href, "appdown/.*")]/@href').extract()
        if referers is not None:
            for referer in set(referers):
                referer = referer if 'http' in referer else 'http://apk.hiapk.com' + referer
                yield scrapy.Request(url=referer, callback=self.parse_item, method='HEAD',
                                      dont_filter=True, priority=1, errback=self.err_back,
                                      meta={'dont_redirect': True, 'dont_obey_robotstxt': True,
                                            'handle_httpstatus_list': (301, 302, 303, 307),
                                            'dont_proxy': self.dont_proxy})

    def parse_item(self, response):
        self.logger.info('current parse_item url: {0}'.format(response.url))

        if 'Location' not in response.headers:
            return None

        location = safe_url_string(response.headers['location'])

        # redirected_url = urljoin(response.url, location)
        redirected_url = location
        download_url = redirected_url
        try:
            package_name = download_url.split('/')[-1].split('_')[0]
            version_code = download_url.split('/')[-1].split('_')[-1].split('.')[0]
            item = HiApkItem()
            item['package_name'] = package_name
            item['version_code'] = version_code
            item['download_url'] = download_url
            return item
        except:
            return None

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

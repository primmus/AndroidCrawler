# coding = utf-8

import os
import logging
import sys
from logging.handlers import RotatingFileHandler

import scrapy
from AndroidCrawler.items import HiapkItem
from six.moves.urllib.parse import urljoin
from w3lib.url import safe_url_string

from AndroidCrawler.conf import config

reload(sys)
sys.setdefaultencoding('utf8')


class NewSpider(scrapy.Spider):
    """hiapk new spider, crawl new apks"""

    name = 'hiapk.newspider'
    allowed_domains = ['hiapk.com']
    categorys = {'apps', 'apps/MediaAndVideo', 'apps/DailyLife', 'apps/Social', 'apps/Finance',
                 'apps/Tools', 'apps/TravelAndLocal', 'apps/Communication', 'apps/Shopping',
                 'apps/Reading', 'apps/Education', 'apps/NewsAndMagazines', 'apps/HealthAndFitness',
                 'apps/AntiVirus', 'apps/Browser', 'apps/Productivity', 'apps/Personalization',
                 'apps/Input', 'apps/Photography',
                 'games', 'games/OnlineGames', 'games/Casual', 'games/RolePlaying', 'games/BrainAndPuzzle',
                 'games/Shooting', 'games/Sports', 'games/Children', 'games/Chess', 'games/Strategy',
                 'games/Simulation', 'games/Racing'}

    def __init__(self, *args, **kwargs):
        super(NewSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://apk.hiapk.com/{0}?sort=9&pi=1'.format(category) for category in self.categorys]
        logger = logging.getLogger(self.name)
        self.__init_logger(logger)

    def __init_logger(self, logger):
        log_dir = config.LOG_DIR + 'hiapk/'
        log_file = log_dir + self.name + '.log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_hander = RotatingFileHandler(log_file, maxBytes=config.LOG_FILE_SIZE,
                                         backupCount=config.LOG_FILE_BACKUP_COUNT)
        log_hander.setLevel(config.LOG_LEVER)
        log_hander.setFormatter(config.LOG_FORMAT)
        logger.addHandler(log_hander)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        referers = response.xpath('//a[re:match(@href, "appdown/.*")]/@href').extract()
        if referers is not None:
            for referer in set(referers):
                yield response.follow(url=referer, callback=self.parse_item, method='HEAD', dont_filter=True,
                                      meta={'dont_redirect': True, 'dont_obey_robotstxt': True,
                                            'handle_httpstatus_list': (301, 302, 303, 307)})

        follows = response.xpath('//div[@class="page"]/a[re:match(@href, "\?sort=9")]/@href').extract()
        if follows is not None:
            for follow in set(follows):
                yield response.follow(follow, callback=self.parse)

    def parse_item(self, response):
        self.logger.info('current parse_item url: {0}'.format(response.url))

        if 'Location' not in response.headers:
            return None

        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(response.url, location)

        download_url = redirected_url
        try:
            package_name = download_url.split('/')[-1].split('_')[0]
            version_code = download_url.split('/')[-1].split('_')[-1].split('.')[0]
            item = HiapkItem()
            item['spider_name'] = self.name
            item['package_name'] = package_name
            item['version_code'] = version_code
            item['download_url'] = download_url
            return item
        except:
            return None
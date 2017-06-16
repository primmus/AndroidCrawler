# coding = utf-8

import json
import random
import scrapy
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.spiders.base.categoryspider import BaseCategorySpider
from AndroidCrawler.db.mumayi import SqlMuMaYi
from AndroidCrawler.items import MuMaYiItem


class CategorySpider(BaseCategorySpider):
    """category spider for Market_Mumayi"""

    name = 'Market_Mumayi.categoryspider'
    market = 'Market_Mumayi'
    allowed_domains = ['mumayi.com']

    download_delay = 15
    download_host = ('http://apka.mumayi.com', 'http://apkb.mumayi.com', 'http://apkc.mumayi.com')

    def __init__(self, **kwargs):
        super(CategorySpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlMuMaYi()
        self._init_start_urls()

    def _init_start_urls(self):
        # 精选
        for page in range(1, 500):
            url = 'http://xml.mumayi.com/v19/index.php?page={0}'.format(page)
            self.start_urls.append(url)
        # 最近很火 精品手游
        for list_type in [1, 2]:
            for page in range(1, 10):
                url = 'http://xmlso.mumayi.com/v18/specialtopics/list.php?type={0}&page={1}'.format(list_type, page)
                self.start_urls.append(url)
        # 金蛋专区
        for page in range(1, 600):
            url = 'http://xml.mumayi.com/v19/list.php?listtype=goodgame&page={0}'.format(page)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back)
        categorys = {('newgame', 250), ('newsoft', 150), ('pushgame', 180),
                     ('pushsoft', 150), ('hotgame', 2500), ('hotsoft', 7000)}
        for list_type, total_page in categorys:
            for page in range(1, total_page):
                url = 'http://xml.mumayi.com/v19/list.php?listtype={0}&page={1}'.format(list_type, page)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                     meta={'dont_proxy': self.dont_proxy},
                                     errback=self.err_back)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        try:
            apps = json.loads(response.text)
            for key, app in apps.items():
                item = MuMaYiItem(app_id=app.get('id'), package_name=app.get('packagename'),
                                  version_code=app.get('versioncode'), app_name=app.get('title'),
                                  download_url=app.get('download'))
                if item.get('download_url') is not None:
                    item['download_url'] = urlparse.urljoin(random.choice(self.download_host), item.get('download_url'))
                    yield item
        except:
            pass

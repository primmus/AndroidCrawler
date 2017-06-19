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

from AndroidCrawler.spiders.base.updatespider import BaseUpdateSpider
from AndroidCrawler.db.mumayi import SqlMuMaYi
from AndroidCrawler.items import MuMaYiItem


class UpdateSpider(BaseUpdateSpider):
    """update spider for Market_Mumayi"""

    name = 'Market_Mumayi.updatespider'
    market = 'Market_Mumayi'
    allowed_domains = ['mumayi.com']

    download_delay = 5
    download_host = ('http://apka.mumayi.com', 'http://apkb.mumayi.com', 'http://apkc.mumayi.com')

    def __init__(self, **kwargs):
        super(UpdateSpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlMuMaYi()
        self._init_start_urls()

    def _init_start_urls(self):
        pass

    def start_requests(self):
        for pkg, app_id in self._get_pkg():
            if not pkg or not app_id:
                continue
            url = 'http://xml.mumayi.com/v19/content.php?packagename={0}&id={1}'.format(pkg, app_id)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back)

    # def _get_pkg(self):
    #     invalid_count, offset, limit = 0, 0, 5000
    #     while invalid_count < 3:
    #         pkg_pool = self.sql_helper.query_pkgs(offset=offset*limit, limit=limit)
    #         offset += 1
    #         invalid_count = 0 if pkg_pool else invalid_count + 1
    #         if pkg_pool:
    #             for pkg in pkg_pool:
    #                 yield pkg

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        try:
            apps = json.loads(response.text)
            for key, app in apps.items():
                item = MuMaYiItem(app_id=app.get('id'), package_name=app.get('packagename'),
                                  version_code=app.get('versioncode'), app_name=app.get('title'),
                                  download_url=app.get('download'))
                if item['download_url'] and item['package_name'] and item['version_code']:
                    item['download_url'] = urlparse.urljoin(random.choice(self.download_host), item.get('download_url'))
                    yield item
        except:
            pass


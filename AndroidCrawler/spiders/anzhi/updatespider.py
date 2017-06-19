# coding: utf-8

import json
import scrapy
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.spiders.base.updatespider import BaseUpdateSpider
from AndroidCrawler.db.anzhi import SqlAnZhi
from AndroidCrawler.items import AnZhiItem


class UpdateSpider(BaseUpdateSpider):
    """category spider for Market_Anzhi"""

    name = 'Market_Anzhi.updatespider'
    market = 'Market_Anzhi'
    allowed_domains = ['anzhi.com']

    download_delay = 10

    def __init__(self, **kwargs):
        super(UpdateSpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlAnZhi()
        self._init_start_urls()

    def _get_pkg(self):
        invalid_count, offset, limit = 0, 0, 5000
        while invalid_count < 3:
            pkg_pool = self.sql_helper.query_pkgs(offset=offset * limit, limit=limit)
            offset += 1
            invalid_count = 0 if pkg_pool else invalid_count+1
            if pkg_pool:
                for pkg in pkg_pool:
                    app_id = self.sql_helper.query_app_id(package_name=pkg)
                    if app_id:
                        yield app_id

    def start_requests(self):
        for app_id in self._get_pkg():
            url = 'http://www.anzhi.com/get_history.php?history_softid={0}'.format(app_id)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        try:
            apps = json.loads(response.text)[0]
            for app in apps:
                try:
                    app_id = app[0]
                    package_name = app[1]
                    version_code = app[6]
                    download_url = app[7]
                    yield AnZhiItem(app_id=app_id, package_name=package_name,
                                    version_code=version_code, download_url=download_url)
                except:
                    pass
        except:
            pass

# coding : utf-8

import scrapy
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.spiders.base.updatespider import BaseUpdateSpider
from AndroidCrawler.db.appchina import SqlAppChina
from AndroidCrawler.items import AppChinaItem


class UpdateSpider(BaseUpdateSpider):
    """update spider for Market_Appchina"""
    name = 'Market_Appchina.updatespider'
    market = 'Market_Appchina'
    allowed_domains = ['appchina.com']
    pkg_pool = []

    def __init__(self, *args, **kwargs):
        super(UpdateSpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlAppChina()
        self._init_start_urls()

    def start_requests(self):
        for pkg in self._get_pkg():
            if not pkg or 'html' in pkg or '?' in pkg:
                continue
            url = 'http://www.appchina.com/app/{0}'.format(pkg)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back, priority=0)

    def parse(self, response):
        self.logger.info('current parse item url: {0}'.format(response.url))

        package_name = urlparse.urlparse(response.url).path.split('/')[-1]

        old_versions = response.xpath('//a[re:match(@class, ".*historyVerison-download.*")]/@href').extract()
        for old_version in old_versions:
            try:
                download_url = old_version
                item = self._parse_download_url(download_url, package_name)
                if item:
                    yield item
            except Exception as e:
                self.logger.warn(e)

        new_version = response.xpath('//a[@class="download_app" and @onclick]/@onclick').extract_first()
        try:
            download_url = None
            for sub_new_app in new_version.split("'"):
                if 'http' in sub_new_app.strip():
                    download_url = sub_new_app.strip()
                    break
            if download_url:
                item = self._parse_download_url(download_url, package_name)
                if item:
                    yield item
        except Exception as e:
            self.logger.warn(e)

    def _parse_download_url(self, download_url, package_name):
        try:
            url_path = urlparse.urlparse(download_url).path.split('/')
            url_path = [sub_url_path for sub_url_path in url_path if sub_url_path]

            version_code = url_path[-1].split('.')[0].split('_')[-1]
            product_id = url_path[2]

            return AppChinaItem(package_name=package_name, product_id=product_id,
                                download_url=download_url, version_code=version_code)
        except Exception as e:
            self.logger.warn(e)

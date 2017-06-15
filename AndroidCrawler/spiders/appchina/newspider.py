# coding : utf-8

import scrapy
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.spiders.base.newspider import BaseNewSpider
from AndroidCrawler.db.appchina import SqlAppChina
from AndroidCrawler.items import AppChinaItem


class NewSpider(BaseNewSpider):
    """new spider for Market_Appchina"""
    name = 'Market_Appchina.newspider'
    market = 'Market_Appchina'
    allowed_domains = ['appchina.com']

    def __init__(self, *args, **kwargs):
        super(NewSpider, self).__init__(name=self.name, market=self.market, *args, **kwargs)
        self.sql_helper = SqlAppChina()
        self._init_start_urls()

    def _init_start_urls(self):
        category = [30, 40, 60]
        category.extend(range(411, 424))
        category.extend(range(301, 316))
        for sub_category in category:
            category_url_pattern = 'http://www.appchina.com/category/' + str(sub_category) + '/{page}_1_1_3_0_0_0.html'
            pages = range(1, 50) if sub_category != 30 and sub_category != 40 else range(1, 168)
            self.start_urls.extend([category_url_pattern.format(page=page) for page in pages])

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        referers = response.xpath('//a[re:match(@href, "/app/.*")]/@href').extract()
        if referers is not None:
            for referer in set(referers):
                referer = response.urljoin(referer)
                # referer = referer if 'http' in referer else 'http://www.appchina.com' + referer
                yield scrapy.Request(url=referer, callback=self.parse_item, dont_filter=True, priority=1,
                                      errback=self.err_back, meta={'dont_proxy': self.dont_proxy})

    def parse_item(self, response):
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

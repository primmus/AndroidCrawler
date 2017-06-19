# coding: utf-8

import scrapy
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse
from w3lib.url import safe_url_string

from AndroidCrawler.spiders.base.newspider import BaseNewSpider
from AndroidCrawler.db.anzhi import SqlAnZhi
from AndroidCrawler.items import AnZhiItem


class NewSpider(BaseNewSpider):
    """category spider for Market_Anzhi"""

    name = 'Market_Anzhi.newspider'
    market = 'Market_Anzhi'
    allowed_domains = ['anzhi.com']

    download_delay = 5

    categorys = [49, 82, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54,
                55, 21, 14, 15, 16, 19, 20, 24, 56, 57]

    def __init__(self, **kwargs):
        super(NewSpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlAnZhi()
        self._init_start_urls()

    def _init_start_urls(self):
        self.start_urls.append('http://www.anzhi.com/list_1_1_new.html')
        self.start_urls.append('http://www.anzhi.com/list_2_1_new.html')
        self.start_urls.extend(['http://www.anzhi.com/sort_{0}_1_{1}.html'.format(category, rank) for category in self.categorys for rank in ['new']])

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        apps = response.xpath('//div[@class="pop_code"]/@rel').extract()
        for app in apps:
            try:
                url_parser = urlparse.parse_qs(urlparse.urlparse(app).query)
                app_id = url_parser.get('softid')[0]
                url = url_parser.get('url')[0]
                package_name = urlparse.parse_qs(urlparse.urlparse(url).query).get('pkg')[0]

                item = AnZhiItem(app_id=app_id, package_name=package_name, version_code=None)
                referer = urlparse.urljoin('http://www.anzhi.com/', '/dl_app.php?s={0}&n=5'.format(app_id))
                yield scrapy.Request(url=referer, callback=self.parse_item, method='HEAD',
                                     priority=1, errback=self.err_back,
                                     meta={'dont_redirect': True, 'dont_obey_robotstxt': True,
                                           'handle_httpstatus_list': (301, 302, 303, 307),
                                           'dont_proxy': self.dont_proxy, 'item': item})
            except:
                pass

        next_page = response.xpath('//div[@class="pagebars"]/a[@class="next"]/@href').extract_first()
        if next_page:
            next_page = urlparse.urljoin('http://www.anzhi.com/', next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True,
                                 meta={'dont_proxy': self.dont_proxy},
                                 errback=self.err_back)

    def parse_item(self, response):
        self.logger.info('current parse_item url: {0}'.format(response.url))

        item = response.meta.get('item')
        if not item:
            return None

        if 'Location' not in response.headers:
            return None

        location = safe_url_string(response.headers['location'])
        if location:
            item['download_url'] = location
            return item

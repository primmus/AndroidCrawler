# coding = utf-8

import sys
import scrapy
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin

from AndroidCrawler.items import HiapkItem

reload(sys)
sys.setdefaultencoding('utf8')
class CategorySpider(scrapy.Spider):
    """hiapk category spider, crawl all apks"""

    name = 'hiapk.categoryspider'
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
        super(CategorySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://apk.hiapk.com/{0}'.format(category) for category in self.categorys]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.logger.info('current parse url: {0}'.format(response.url))

        referers = response.xpath('//a[re:match(@href, "appdown/.*")]/@href').extract()
        if referers is not None:
            for referer in set(referers):
                yield response.follow(url=referer, callback=self.parse_item, method='HEAD',
                                dont_filter=True, meta={'dont_redirect': True})

        follows = response.xpath('//a[re:match(@href, "(apps|games).*\?.*")]/@href').extract()
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
            return item
        except:
            return None

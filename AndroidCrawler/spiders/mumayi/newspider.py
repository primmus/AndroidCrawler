# coding = utf-8

import json
import random
try:
    # for python2
    import urlparse
except:
    # for python3
    import urllib.parse as urlparse

from AndroidCrawler.spiders.base.newspider import BaseNewSpider
from AndroidCrawler.db.mumayi import SqlMuMaYi
from AndroidCrawler.items import MuMaYiItem


class NewSpider(BaseNewSpider):
    """new spider for Market_Mumayi"""

    name = 'Market_Mumayi.newspider'
    market = 'Market_Mumayi'
    allowed_domains = ['mumayi.com']

    download_delay = 30
    download_host = ('http://apka.mumayi.com', 'http://apkb.mumayi.com', 'http://apkc.mumayi.com')

    def __init__(self, **kwargs):
        super(NewSpider, self).__init__(name=self.name, market=self.market, **kwargs)
        self.sql_helper = SqlMuMaYi()
        self._init_start_urls()

    def _init_start_urls(self):
        for list_type in ['newgame', 'newsoft']:
            for page in range(1, 200):
                url = 'http://xml.mumayi.com/v19/list.php?listtype={0}&page={1}'.format(list_type, page)
                self.start_urls.append(url)
        pass

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

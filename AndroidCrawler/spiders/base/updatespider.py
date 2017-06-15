# coding = utf-8

from AndroidCrawler.spiders.base.newspider import BaseNewSpider


class BaseUpdateSpider(BaseNewSpider):
    """update spider module"""

    def _init_start_urls(self):
        self.start_urls = []

    def _get_pkg(self):
        invalid_count, offset, limit = 0, 0, 5000
        while invalid_count < 3:
            pkg_pool = self.sql_helper.query_pkgs(offset=offset * limit, limit=limit)
            offset += 1
            invalid_count = 0 if pkg_pool else invalid_count+1
            if pkg_pool:
                for pkg in pkg_pool:
                    yield pkg

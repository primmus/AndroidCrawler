
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from AndroidCrawler.spiders import hiapk
from AndroidCrawler.spiders import a360
from AndroidCrawler.spiders import appchina


log = logging.getLogger('runspiders')


def main():
    try:
        process = CrawlerProcess(get_project_settings())
        # # Market_Hiapk
        # process.crawl(hiapk.CategorySpider)
        # process.crawl(hiapk.NewSpider)
        # process.crawl(hiapk.UpdateSpider)
        # # Market_360
        # process.crawl(a360.CategorySpider)
        # process.crawl(a360.NewSpider)
        # process.crawl(a360.UpdateSpider)
        # Market_Appchina
        process.crawl(appchina.NewSpider)
        process.crawl(appchina.CategorySpider)
        # process.crawl(appchina.UpdateSpider)
        #
        process.start()
    except Exception as e:
        log.error(e)


if __name__ == "__main__":
    main()

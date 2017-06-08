
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from AndroidCrawler.spiders import hiapk


log = logging.getLogger('runspiders')


def main():
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(hiapk.CategorySpider)
        process.crawl(hiapk.NewSpider)
        process.crawl(hiapk.UpdateSpider)
        process.start()
    except Exception:
        pass


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    download_url = scrapy.Field()
    package_name = scrapy.Field()
    version_code = scrapy.Field()
    pass


class HiApkItem(BaseItem):
    pass

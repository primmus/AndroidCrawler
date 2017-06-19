# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    download_url = scrapy.Field()
    package_name = scrapy.Field()
    version_code = scrapy.Field()
    pass


class HiApkItem(BaseItem):
    pass


class A360Item(BaseItem):
    product_id = scrapy.Field()
    app_md5 = scrapy.Field()
    pass


class MuMaYiItem(BaseItem):
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    pass


class AppChinaItem(BaseItem):
    product_id = scrapy.Field()
    pass


class AnZhiItem(BaseItem):
    app_id = scrapy.Field()
    pass

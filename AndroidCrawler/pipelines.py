# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from scrapy.exceptions import DropItem

from AndroidCrawler.db.hiapk import SqlHiApk


_sql_hi_apk = SqlHiApk()


class CommonPipeline(object):
    """check item if exists in db"""
    def process_item(self, item, spider):
        row = _sql_hi_apk.item_to_row(item)
        if row:
            download_flag, collect_time, distributed_id = _sql_hi_apk.query_download_status(row)
            if download_flag == 1:
                raise DropItem('item has been downloaded: {item}'.format(item=item))
            elif download_flag == 0 and (datetime.datetime.utcnow()-collect_time).days <= 0:
                raise DropItem('item has been collected: {item}'.format(item=item))

            spider.logger.info('new item to collect: {item}'.format(item=item))
            if download_flag < 0:
                # new item, add to table
                _sql_hi_apk.add(row)
            else:
                # old item, assign distributed_id
                row.Distributed_id = distributed_id

            if row.distributed_id is not None:
                _sql_hi_apk.add_to_dis_crawler_tasks(row)
        return item

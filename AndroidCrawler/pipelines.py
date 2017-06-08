# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from scrapy.exceptions import DropItem


class CommonPipeline(object):
    """check item if exists in db"""
    def process_item(self, item, spider):
        sql_helper = getattr(spider, 'sql_helper', None)
        if not sql_helper:
            raise DropItem('sql helper has been is None: {item}'.format(item=item))
        row = sql_helper.item_to_row(item)
        if row:
            download_flag, collect_time, distributed_id = sql_helper.query_download_status(row)
            if download_flag == 1:
                raise DropItem('item has been downloaded: {item}'.format(item=item))
            elif download_flag == 0 and (datetime.datetime.utcnow()-collect_time).days <= 0:
                raise DropItem('item has been collected: {item}'.format(item=item))

            spider.logger.info('new item to collect: {item}'.format(item=item))
            if download_flag < 0:
                # new item, add to table
                sql_helper.add(row)
            else:
                # old item, assign distributed_id
                row.Distributed_id = distributed_id

            if row.distributed_id is not None:
                sql_helper.add_to_dis_crawler_tasks(row)
        return item

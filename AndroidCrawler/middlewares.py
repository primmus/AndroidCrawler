# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if 'robots' in request.url:
            return 
        if not hasattr(spider, 'proxy_pool'):
            return
        if request.meta.get('dont_proxy', False):
            return
        if 'proxy' in request.meta:
            return
        sql_helper = getattr(spider, 'sql_helper', None)
        validator = getattr(spider, 'validator', None)
        if not sql_helper or not validator:
            return

        proxy_pool_update_time = getattr(spider, 'proxy_pool_update_time', None)
        proxy_pool = getattr(spider, 'proxy_pool')

        if not proxy_pool_update_time or (time.time() - proxy_pool_update_time) > 60*10:
            proxy_pool = sql_helper.query_proxy_by_validator(validator)
            if proxy_pool:
                setattr(spider, 'proxy_pool', proxy_pool)
                setattr(spider, 'proxy_pool_update_time', time.time())
            spider.logger.info('update proxy pool: {0} proxy in pool.'.format(len(proxy_pool)))

        if proxy_pool:
            proxy = random.choice(proxy_pool)
            request.meta['proxy'] = 'http://%s:%s' % proxy
            return request

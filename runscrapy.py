# -*- coding: utf-8 -*-

import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


from AndroidCrawler.conf import config


def run_scrapy(name):
    logger = logging.getLogger('runscrapy')
    log_config = config.LOG_CONFIG
    if not os.path.exists('log'):
        os.makedirs('log')
    log_file = 'log/runscrapy.log'
    log_hander = RotatingFileHandler(log_file, maxBytes=log_config.get('LOG_FILE_SIZE', 10 * 1024 * 1024),
                                     backupCount=log_config.get('LOG_FILE_BACKUP_COUNT', 3))
    log_hander.setLevel(log_config.get('LOG_LEVER', logging.DEBUG))
    log_hander.setFormatter(log_config.get('LOG_FORMAT'))
    logger.addHandler(log_hander)

    process = CrawlerProcess(get_project_settings())
    try:
        logger.info('runscrapy start spider:%s' % name)
        process.crawl(name)
        process.start()
    except Exception as e:
        logger.error('runscrapy spider:%s exception:%s' % (name, e))
        pass
    logger.info('finish this spider:%s\n\n' % name)


if __name__ == '__main__':
    name = sys.argv[1] or 'base'
    print('name:%s' % name)
    print ('project dir:%s' % os.getcwd())
    run_scrapy(name)

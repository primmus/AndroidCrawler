# coding: utf-8

import os
import logging
import time
import subprocess
from logging.handlers import RotatingFileHandler

from AndroidCrawler.conf import config
from AndroidCrawler.spiders import a360
from AndroidCrawler.spiders import hiapk
from AndroidCrawler.spiders import appchina


def main():
    logger = logging.getLogger('runcrawler')
    log_config = config.LOG_CONFIG
    if not os.path.exists('log'):
        os.makedirs('log')
    log_file = 'log/runcrawler.log'
    log_hander = RotatingFileHandler(log_file, maxBytes=log_config.get('LOG_FILE_SIZE', 10 * 1024 * 1024),
                                     backupCount=log_config.get('LOG_FILE_BACKUP_COUNT', 3))
    log_hander.setLevel(log_config.get('LOG_LEVER', logging.DEBUG))
    log_hander.setFormatter(log_config.get('LOG_FORMAT'))
    logger.addHandler(log_hander)

    spiders = [
        a360.CategorySpider,
        a360.NewSpider,
        a360.UpdateSpider,
        hiapk.CategorySpider,
        hiapk.UpdateSpider,
        hiapk.NewSpider,
        appchina.NewSpider,
        appchina.CategorySpider,
        appchina.UpdateSpider
    ]

    process_list = []
    for spider in spiders:
        popen = subprocess.Popen(['python', 'runscrapy.py', spider.name], shell=False)
        data = {
            'name': spider.name,
            'popen': popen,
        }
        process_list.append(data)

    logger.info(process_list)

    while True:
        try:
            for process in process_list:
                popen = process.get('popen', None)
                logger.info('name:%s poll:%s' % (process.get('name'), popen.poll()))
                #  检测结束进程，如果有结束进程，重新开启
                if popen is not None and popen.poll() == 0:
                    name = process.get('name')
                    logger.info('%(name)s spider finish...\n' % {'name': name})
                    process_list.remove(process)
                    p = subprocess.Popen(['python', 'runscrapy.py', name], shell=False)
                    data = {
                        'name': name,
                        'popen': p,
                    }
                    process_list.append(data)
                    time.sleep(5)
                    break
            time.sleep(60 * 60 * 12)
            pass
        except Exception as e:
            logger.warn('Exception %s' % str(e))

if __name__ == "__main__":
    main()

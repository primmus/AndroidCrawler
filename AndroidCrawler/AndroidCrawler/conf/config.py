# coding: utf-8

import logging

LOG_DIR = 'log/'
LOG_FILE_SIZE = 10*1024*1024
LOG_FILE_BACKUP_COUNT = 3
LOG_LEVER = logging.DEBUG
LOG_FORMAT = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')

# LOG_HANDLER = RotatingFileHandler(LOG_DIR, maxBytes=LOG_FILE_SIZE, backupCount=LOG_FILE_BACKUP_COUNT)





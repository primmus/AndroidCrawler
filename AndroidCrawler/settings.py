# -*- coding: utf-8 -*-

# Scrapy settings for AndroidCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AndroidCrawler'

SPIDER_MODULES = ['AndroidCrawler.spiders']
NEWSPIDER_MODULE = 'AndroidCrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AndroidCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en;zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0.14393; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2950.5 Safari/537.36'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AndroidCrawler.middlewares.AndroidcrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'AndroidCrawler.middlewares.ProxyMiddleware': 100,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy_jsonrpc.webservice.WebService': 500,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'AndroidCrawler.pipelines.CommonPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# The amount of time (in secs) that the downloader will wait before timing out. Default: 180
DOWNLOAD_TIMEOUT = 60

# The maximum response size (in bytes) that downloader will download. Default: 1073741824 (1024MB) disable it set to 0.
# DOWNLOAD_MAXSIZE = 1073741824

# LOG_ENABLED = True
# LOG_ENCODING = 'utf-8'
# LOG_FILE = 'scrapy.log'
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# LOG_LEVEL = 'DEBUG'
# LOG_STDOUT = True

# MEMDEBUG_ENABLED = True

# A boolean which specifies if the web service will be enabled (provided its extension is also enabled).
# Default: False
JSONRPC_ENABLED = False
# A file to use for logging HTTP requests made to the web service. If unset web the log is sent to standard scrapy log.
# Default: None
JSONRPC_LOGFILE = 'webservice.log'
# The port range to use for the web service. If set to None or 0, a dynamically assigned port is used.
# Default: [6080, 7030]
JSONRPC_PORT = [6080, 7030]
# The interface the web service should listen on.
# Default: '127.0.0.1'
JSONRPC_HOST = '127.0.0.1'




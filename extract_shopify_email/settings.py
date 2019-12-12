# -*- coding: utf-8 -*-

# Scrapy settings for extract_shopify_email project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'extract_shopify_email'

DOWNLOAD_TIMEOUT = 15

SPIDER_MODULES = ['extract_shopify_email.spiders']
NEWSPIDER_MODULE = 'extract_shopify_email.spiders'

RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 430]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {

  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6',
  'Cache-Control': 'max-age=0',
  'cookie': 'skin=noskin; session-id=146-5212703-9842164; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=130-9773620-7068244; x-wl-uid=1Rre102S/ujRozgKwTU1Y9c8kCEdw8Zu0jT3vZBN8890CoS1LDYot/IXRcbEJTGcCfrB5Rsm+oiw=; s_cc=true; s_nr=1573615300210-New; s_vnum=2005615300211%26vn%3D1; s_dslv=1573615300212; s_sq=%5B%5BB%5D%5D; session-token=A7E4GuamYKuaoAss+sjY9wMBXPiGRWbOOeWCuH/cjBFkGvm17UFynjuFiuGCagyeH1KZrCf/OMPXZOUZaekFNysw5x86EVNMdJ4vH99EmbdX/uUOtvPBPSWqJYMrCwYK5+qMYt4eLstk8pWA0NBl3W6bMBQi0oKOBT1fbRYVS3kjpao1rz2gfmL0kGT5cM+8sOhKkYqgsn5KrFK8r/qD2QaxX+P9nQJa; csm-hit=tb:8ABWC9QNP2GWRD5HS1RK+s-JS22G0J5ZWTY8GP93ARN|1573623964625&t:1573623964625&adb:adblk_yes',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'Content-Type': 'text/html; charset=utf-8'
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CONCURRENT_REQUESTS_PER_IP = 10

LOG_LEVEL = 'DEBUG'
# LOG_FILE = './logger.log'
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'extract_shopify_email.middlewares.ExtractShopifyEmailSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'extract_shopify_email.middlewares.ExtractShopifyEmailDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'extract_shopify_email.pipelines.ExtractShopifyEmailPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10

# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

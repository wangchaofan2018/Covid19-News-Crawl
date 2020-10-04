# Scrapy settings for covid_19 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'covid_19'

SPIDER_MODULES = ['covid_19.spiders']
NEWSPIDER_MODULE = 'covid_19.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'covid_19 (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_ENABLED=True
# 日志格式
LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 日志时间格式
LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'

# 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL='DEBUG'
# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
LOG_STDOUT=True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'Cookie':'Secure; FSSBBIl1UgzbN7N80S=imwotUDjy5a161oG.QO.IKWMNQmZg.t8fFEKmivRMbMaYvQmfsJpg9oeIx.aE2XO; Secure; _trs_uv=kftg7k30_3027_i9ke; _trs_ua_s_1=kftwww.hubei.gov.cn7k30_3027_fwh6; Hm_lvt_5544783ae3e1427d6972d9e77268f25d=1601715763; dataHide2=bcbf7a5c-77fd-4157-9a66-4b2d6fad92ab; Hm_lpvt_5544783ae3e1427d6972d9e77268f25d=1601717455; FSSBBIl1UgzbN7N80T=4Nq9DHQtXC3Dq5ZfMV4rPELVHaTyM4Cz7LjuvhN1EhZVw.qqUHkOuYELP7nrfsWG_Fj2xL.Bkve_14D0vDzExFmSYZUWWspts0YSd2olgDww5_QQTBMrUS6FRMhHV6_OLaJ6XoQ6eQFj8.Zdgibg4xWjP_ohJXq9G1UtWYbAQbq2nU0YYpcF5vo4Tp2mqikdpmhUEmo9OpBt5ZrCyv0xlBcT0mIEsaPJHH7QOPomj79wuzE2RQikOSpUE7xcm0PZEcvemW6WcTZWuafPf4ntpsOjN9W7vz8PRcRjOFj89.i5tH9J81ziOKM.f8a4nOrrGAMdbHwdadnSYwHKGOBFqVXGw03WuOAF9TY3IvlWFR7oBSdEvJt7n75OqHJaDzk7AhDn_smESr_nRR3ZI4.vfypKb',
  'Host':'www.hubei.gov.cn'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'covid_19.middlewares.Covid19SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
	'covid_19.middlewares.BrowserDownloaderMiddleware': 443,
   # 'covid_19.middlewares.Covid19DownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'covid_19.pipelines.BaseDataPipeline': 300,
}

MONGO_DB_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "covid19_info_data"
MONGO_COLLECTION_NAME = "news"



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

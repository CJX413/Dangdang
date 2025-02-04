# -*- coding: utf-8 -*-

# Scrapy settings for dangdang project

BOT_NAME = 'dangdang'

SPIDER_MODULES = ['dangdang.spiders']
NEWSPIDER_MODULE = 'dangdang.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 调度
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 去重
SCHEDULER_PERSIST = True  # 不清理Redis队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"  # 队列
ITEM_PIPELINES = {
    'dangdang.pipelines.DangdangPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'dangdang.middlewares.DangdangSpiderMiddleware': 100,
}
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'dangdang'
MONGODB_DOCNAME = "saveinto_2"

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

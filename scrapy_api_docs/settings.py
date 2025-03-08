# settings.py for Scrapy
BOT_NAME = 'scrapy_api_docs'

SPIDER_MODULES = ['scrapy_api_docs.spiders']
NEWSPIDER_MODULE = 'scrapy_api_docs.spiders'

# set the User-Agent (optional)
# USER_AGENT = 'my-scraper (+http://example.com)'

ITEM_PIPELINES = {
    'scrapy_api_docs.pipelines.ApiScraperPipeline': 1,
}


DOWNLOAD_DELAY = 2

# Enable logging to save logs to a file
LOG_FILE = "logs/scraping_log.txt"
LOG_LEVEL = 'INFO'

RETRY_HTTP_CODES = [400, 404]


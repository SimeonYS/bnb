BOT_NAME = 'bnb'

SPIDER_MODULES = ['bnb.spiders']
NEWSPIDER_MODULE = 'bnb.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0
USER_AGENT="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'bnb.pipelines.BnbPipeline': 300,

}
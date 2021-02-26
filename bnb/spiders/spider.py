import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BnbItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class BnbSpider(scrapy.Spider):
	name = 'bnb'
	start_urls = ['https://www.bnb.bg/PressOffice/POStatements/POADate/index.htm',
				  'https://www.bnb.bg/PressOffice/POPressReleases/POPRDate/index.htm'
				  ]

	def parse(self, response):
		post_years = response.xpath('//div[@class="top"]//a/@href').getall()
		yield from response.follow_all(post_years, self.parse_links)

	def parse_links(self, response):
		articles = response.xpath('//div[@class="content"]/h3/a')
		for article in articles:
			date = article.xpath('.//text()').get()
			post_links = article.xpath('.//@href').get()
			yield response.follow(post_links, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response,date):

		title = response.xpath('//p[contains(@style,"text-align: center;")]//text() |//span[@style="color: Maroon"]//text()').getall()
		title = ' '.join([text.strip() for text in title if text.strip()])
		content = response.xpath('//p[contains(@style,"text-align: justify; text-indent: ")]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=BnbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()

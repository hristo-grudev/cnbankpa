import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import CnbankpaItem
from itemloaders.processors import TakeFirst


class CnbankpaSpider(scrapy.Spider):
	name = 'cnbankpa'
	start_urls = ['https://www.cnbankpa.com/About/Explore-C-N/Press-Releases']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="UnselectedNext"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="container main"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = re.findall(r'[A-Za-z]+\s\d{1,2},\s\d{4}', description) or ['']

		item = ItemLoader(item=CnbankpaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date[0])

		return item.load_item()

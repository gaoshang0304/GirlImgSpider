# coding= utf-8
from multiprocessing import Pool

import scrapy
import time
from scrapy.http import Request  ##一个单独的request的模块，需要跟进URL的时候，需要用它
from scrapy.selector import Selector
from demoSpider.items import DemospiderItem


class MySpider(scrapy.Spider):
	# 爬虫名
	name = "demoSpider"
	# 基础url
	host = "http://www.7160.com/"
	start_urls = ['http://www.7160.com/rentiyishu/list_1_1.html']

	def start_requests(self):
		for i in range(65):
			yield Request('http://www.7160.com/rentiyishu/list_1_%s.html' % str(i), callback=self.parse)

	def parse(self, response):
		selector = Selector(response)
		href_list = selector.xpath('//div[@class="new-img"]/ul/li/a/@href').extract()
		for href in href_list:
			url = self.host + href
			yield Request(url, callback=self.parse_single)

	def parse_single(self, response):
		print response.url
		selector = Selector(response)
		img_list = selector.xpath('//div[@class="itempage"]/a//text()').extract()
		for img_page in img_list:
			if img_page.isdigit():
				url = response.url + "index_" + img_page + ".html"
				yield Request(url, callback=self.parse_img)

	def parse_img(self, response):
		imgItem = DemospiderItem()
		selector = Selector(response)
		img_url = selector.xpath('//div[@class="picsbox picsboxcenter"]/p/a/img/@src').extract_first()
		imgItem['image_url'] = img_url
		imgItem['image_name'] = img_url[-18:-4]

		yield imgItem

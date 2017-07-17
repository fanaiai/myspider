import scrapy
from scrapy_splash import SplashRequest
from myspider.items import YihaoItem,JdItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
import re
import json

class yihaoSpider(scrapy.Spider):
	name="yihaospider"
	list_urls=["http://www.yhd.com/marketing/allproduct.html"]
	start_urls=["http://list.yhd.com/c0-0-87589//?tp=2092.0.0.0.0.LpFfcyt-10-CnDQc&ti=3W7K5x"]

	def start_requests(self):
		for u in self.start_urls:
			yield scrapy.Request(u,callback=self.parse_page)

	def parse_page(self,response):
		totalPage=response.css("#lastPage::text").extract_first()
		for i in range(1,int(totalPage)):
			url='%s#page=%s&sort=1' % (response.url,i)
			print('----------')
			print(url)
			yield scrapy.Request(url,callback=self.parse_list,dont_filter=True)

	def parse_list(self,response):
		alllists=response.css("#itemSearchList>div")
		print("+++++++++++++++++++++++++++")
		print(alllists)
		for l in alllists:
			print(l.css("::attr('id')").extract_first())


	def parse_cats(self,response):
		allsorts=response.css(".alonesort .mc em a");
		item=YihaoItem()
		for l in allsorts:
			item['url']=response.urljoin(l.css("::attr('href')").extract_first())
			item['name']=l.css("::text").extract_first()
			print(item)
			yield item



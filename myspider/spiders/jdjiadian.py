import scrapy
from scrapy.selector import Selector
from myspider.items import JiadianItem
from scrapy.utils.response import open_in_browser
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
from scrapy_splash import SplashRequest

class JdjiadianSpider(scrapy.Spider):
	name="jiadian"

	headers={}

	start_urls=['https://jiadian.jd.com/']

	def parse(self,response):
		print('startparse---------------------------------------')
		with open('index.html','wb') as f:
			f.write(response.body)
		for i,url in enumerate(Selector(response).re(r'URL":"(https[^"]*cat[^"]*)"')):
			# if i<1:
			print(url.replace('\\',''))
			yield scrapy.Request(url.replace('\\',''),callback=self.parse_class)

	def parse_class(self,response):
		print('startparseclass---------------------------------')
		with open('list.html','wb') as f:
			f.write(response.body)
		for item in response.css("#plist .p-name a::attr(href)").extract():
			url=response.urljoin(item)
			yield SplashRequest(url,callback=self.parse_item, args={'wait': 5.5})

		for item in response.css('.pn-next::attr(href)').extract():
			url=response.urljoin(item)
			yield scrapy.Request(url,callback=self.parse_class)

	def parse_item(self,response):
		print('startparseitem---------------------------------')
		# with open('obj.html','w',encoding='gbk') as f:
		# 	f.write(response.body.decode('gbk'))
		# print(response.css('.price::text').extract_first())
		print(response.css('.price'))
		l=ItemLoader(item=JiadianItem(), response=response)
		l.add_css('name','.sku-name::text', TakeFirst())
		l.add_css('id','.follow::attr(data-id)', TakeFirst())
		l.add_css('price','.price::text', TakeFirst())
		l.add_css('brand','#parameter-brand a::text', TakeFirst())
		l.add_css('parameter','.p-parameter-list li::text')
		l.add_css('summary_service','#summary-service span::text', TakeFirst())
		l.add_value('url',response.url)
		return l.load_item()
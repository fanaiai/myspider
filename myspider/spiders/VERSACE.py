import scrapy
from scrapy.selector import Selector
from myspider.items import JiadianItem
from scrapy.utils.response import open_in_browser
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
from scrapy_splash import SplashRequest
import json
class VERSACESpider(scrapy.Spider):
	name='versace'
	page=1
	start_urls=['https://search.jd.com/search?keyword=%E8%8C%83%E6%80%9D%E5%93%B2&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E8%8C%83%E6%80%9D%E5%93%B2&cid3=9188#J_searchWrap']
	script="""
		function main(splash)
			splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js")
			splash:go("http://example.com")
			splash:runjs("$('.pn-next').click()")
			return splash:html()
		end
		"""
	RENDER_HTML_URL="192.168.56.101:8050"
	def start_requests(self):
		for url in self.start_urls:
			body = json.dumps({"url": url, "wait": 0.5}, sort_keys=True)
			print('+++++++++++++++++++++++++++++++++++++++++++++')
			yield SplashRequest(self.RENDER_HTML_URL,callback=self.parse, args={'wait': 5.5},body=body)

	def parse(self,response):
		print('startparseclass---------------------------------')
		open_in_browser(response)
		yield scrapy.Request(self.RENDER_HTML_URL,callback=self.parse,meta={
				'splash':{
					'args':{'lua_source':self.script,'wait': 5.5},
					'endpoint':'execute',
				}
			})

	def parse_item(self,response):
		print('startparseitem---------------------------------')
		# with open('obj.html','w',encoding='gbk') as f:
		# 	f.write(response.body.decode('gbk'))
		# print(response.css('.price::text').extract_first())
		# print(response.css('.price'))
		l=ItemLoader(item=JiadianItem(), response=response)
		l.add_css('name','.sku-name::text', TakeFirst())
		l.add_css('id','.follow::attr(data-id)', TakeFirst())
		l.add_css('price','.price::text', TakeFirst())
		l.add_css('brand','#parameter-brand a::text', TakeFirst())
		l.add_css('parameter','.p-parameter-list li::text')
		l.add_value('parameter','无')
		l.add_css('summary_service','#summary-service span::text', TakeFirst())
		l.add_css('summary_service','#summary-service a::text', TakeFirst())
		l.add_value('summary_service','无')
		l.add_value('url',response.url)
		l.add_value('price','0')
		l.add_value('brand','范思哲（VERSACE）')
		return l.load_item()

import scrapy
from scrapy_splash import SplashRequest
from myspider.items import JdlistItem,JdItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
import re
import json

class Jdspider(scrapy.Spider):
	name="jdspider"

	start_urls=['https://www.jd.com/allSort.aspx']

	prourl="http://192.168.56.100:8050"
	itemindex=0

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url,callback=self.parse,args={
				'wait':2.5,'url':url
				})

	def parse(self,response):
		listscript="""
		function main(splash)
				local url = splash.args.url
				assert(splash:go(url))
				assert(splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js"))
				local scroll_to = splash:jsfunc("window.scrollTo")
				scroll_to(0, 20000)
				assert(splash:wait(5))
				return {
					html = splash:html(),
					a=splash:url(),
					nonext='0',
					str=splash.args
				}
		end
		"""
		lists=response.css('.items dl dd a');
		print('parse--------------------------------------------------')
		for i,l in enumerate(lists):
			url=l.css('::attr(href)').extract_first()
			if(re.search("list.jd.com",url)):
				if(i<10):
					url=response.urljoin(url)
					name=l.css('::text').extract_first()
					yield SplashRequest(url,callback=self.parse_list,meta={'name':name},args={'lua_source':listscript,'url':url,'wait':2.5})

	def parse_list(self,response):
		print('parse_list------------------------------------------')
		itemscript="""
			function main(splash)
				local url = splash.args.url
				assert(splash:go(url))
				assert(splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js"))
				local js='$(".count").trigger("click")'
				assert(splash:runjs(js))
				local scroll_to = splash:jsfunc("window.scrollTo")
				scroll_to(0, 20000)
				assert(splash:wait(5))
				return {
					png=splash:png{width=nil, height=nil, render_all=true, scale_method='raster', region=nil},
					html = splash:html(),
					a=splash:url(),
					nonext='0',
					str=splash.args
				}
			end
			"""
		print(response.url)
		itemlists=response.css('#plist li')
		for i in itemlists:
			url=i.css('.p-name a::attr(href)').extract_first()
			price=i.css('.p-price i::text').extract_first()
			sku=i.css('.j-sku-item::attr(data-sku)').extract_first()
			url = response.urljoin(url)
			print(url)
			yield SplashRequest(url,callback=self.parse_item,endpoint='execute',meta={'price':price,'sku':sku},args={
				'wait':2.5,'url':url,'lua_source':itemscript,'timeout':50
				}) 
		print('parse_page-----------------------------------------')
		listscript="""
		function main(splash)
				local url = splash.args.url
				assert(splash:go(url))
				assert(splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js"))
				local scroll_to = splash:jsfunc("window.scrollTo")
				scroll_to(0, 20000)
				assert(splash:wait(5))
				return {
					html = splash:html(),
					a=splash:url(),
					nonext='0',
					str=splash.args
				}
		end
		"""
		# next_page=response.urljoin(response.css('.pn-next::attr(href)').extract_first())
		# print(next_page)
		# item=JdlistItem()
		# item['name']=response.meta['name']
		# item['url']=response.url
		# print(response.meta['name'])
		# print(response.url)
		# yield item
		# yield SplashRequest(next_page,callback=self.parse_list,endpoint="execute",meta={'name':response.meta['name']},args={
		# 		'wait':2.5,'url':next_page,'lua_source':listscript
		# 		})	
		

	def parse_item(self,response):
		self.itemindex +=1
		print("parse_item--------------------------%s" % self.itemindex)
		print(response.css("#spec-n1 img::attr(src)").extract_first())
		images_url=response.urljoin(response.css("#spec-n1 img::attr(src)").extract_first())
		l=ItemLoader(item=JdItem(), response=response)
		l.add_css('name','#name h1::text', TakeFirst())
		l.add_value('id',response.meta['sku'])
		l.add_css('price','.price::text', TakeFirst())
		l.add_css('brand','#parameter-brand a::text', TakeFirst())
		l.add_css('parameter','.p-parameter-list *::text')
		l.add_value('parameter','无')
		l.add_css('summary_service','#summary-service span::text', TakeFirst())
		l.add_css('summary_service','#summary-service a::text', TakeFirst())
		l.add_css('add_service','#summary-support span::text')
		l.add_value('add_service','无')
		l.add_css('sales_promotion','.p-promotions em.hl_red::text')
		l.add_css('sales_promotion','.prom-item em.hl_red::text')
		l.add_value('sales_promotion','无')
		l.add_css('store','.J-hove-wrap a::text', TakeFirst())
		l.add_css('store_link','.J-hove-wrap a::attr(href)', TakeFirst())
		l.add_value('images_url',images_url)
		l.add_value('images_url','无')
		l.add_value('store','无')
		l.add_value('store_link','无')
		l.add_value('summary_service','无')
		l.add_value('url',response.url)
		l.add_value('price',response.meta['price'])
		l.add_value('brand','怎么回事')
		commenturl='https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv25' % (response.meta['sku'])
		yield scrapy.Request(commenturl,callback=self.parse_comments,meta={'item':l})

	def parse_comments(self,response):
		l=response.meta['item']
		j=json.loads(response.body.decode('gbk').replace('fetchJSON_comment98vv25(','')[0:-2])['productCommentSummary']
		t=json.loads(response.body.decode('gbk').replace('fetchJSON_comment98vv25(','')[0:-2])['hotCommentTagStatistics']
		l.add_value('commentsnum',j['commentCount'])
		l.add_value('goodcomments',j['goodRateShow'])
		l.add_value('goodcommentnum',j['goodCount'])
		l.add_value('mediumcommentnum',j['generalCount'])
		l.add_value('badcommentnum',j['poorCount'])
		l.add_value('commentsnum','0')
		l.add_value('goodcomments','0')
		l.add_value('goodcommentnum','0')
		l.add_value('mediumcommentnum','0')
		l.add_value('badcommentnum','0')
		l.add_value('comment_tags',t)
		l.add_value('comment_tags',"无")
		return l.load_item()
import scrapy
from scrapy_splash import SplashRequest
from scrapy.utils.response import open_in_browser
import webbrowser
import tempfile
import os
import json
# from scrapy_splash.response import open_in_browser
from myspider.items import JiadianItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join

class Myspider(scrapy.Spider):
	name='jditem'
	start_urls=["https://item.jd.com/3133829.html"]
	prourl="http://192.168.99.100:8050"
	index=0
	itemid=0
	commenturl='https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv25' % itemid
	def start_requests(self):
		for i,url in enumerate(self.start_urls):
			script="""
			function main(splash)
			local url = splash.args.url
			assert(splash:go(url))
			local scroll_to = splash:jsfunc("window.scrollTo")
			scroll_to(0, 0)
			assert(splash:wait(5))
			scroll_to(0, 20000)
			assert(splash:wait(5))
			return {
				html = splash:html(),
				a=splash:url(),
				nonext='0'
			}
			end
			"""
			yield SplashRequest(self.prourl,endpoint='execute',callback=self.parse_item,dont_filter=True,magic_response=True,args={
				'url':url,'wait':0.5,'lua_source': script
				})

	def parse(self,response):
		with open('itemlist.html','wb') as f:
			f.write(response.body)
		itemurls=response.css('#J_goodsList .p-name>a::attr(href)').extract()
		itemscript="""
		function main(splash)
			local url = splash.args.url
			assert(splash:go(url))
			local scroll_to = splash:jsfunc("window.scrollTo")
			scroll_to(0, 0)
			assert(splash:wait(2.5))
			scroll_to(0, 20000)
			assert(splash:wait(2.5))
			return {
				png=splash:png{width=nil, height=nil, render_all=true, scale_method='raster', region=nil},
				html = splash:html(),
				a=splash:url(),
				nonext='0'
			}
		end
		"""
		for url in itemurls:
			print('itemurl==============================')
			url=response.urljoin(url)
			yield SplashRequest(self.prourl,endpoint='execute',callback=self.parse_item,dont_filter=True,args={
			'url':url,'wait':2.5,'lua_source':itemscript
			})

		url=response.data['a']
		nonext=response.data['nonext']
		print('url-------------------------------------------')
		print(url)
		print(nonext=="false")
		script="""
		function main(splash)
			local url = splash.args.url
			assert(splash:go(url))
			assert(splash:wait(0.5))
			assert(splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js"))
			local js = '$(".pn-next").click()'
			assert(splash:runjs(js))
			local nonext=splash:evaljs('String($(".pn-next").hasClass("disabled"))')
			return {
				html = splash:html(),
				a=splash:url(),
				nonext=nonext
			}
		end
		"""
		if nonext=="false":
			yield SplashRequest(self.prourl,endpoint='execute',callback=self.parse,dont_filter=True,args={
				'url':url,'wait':0.5,'lua_source': script
				})
		
	def parse_item(self,response):
		self.index +=1
		# with open('itemtest'+str(self.index)+'.html','w',encoding='utf-8-sig') as f:
		# 	f.write(response.data['str'])
		# fd, fname = tempfile.mkstemp(".html")
		# os.write(fd, response.body)
		# os.close(fd)
		# webbrowser.open("file://%s" % fname)
		print('startparseitem---------------------------------')
		print(response.css('#i-comment *::text').extract())
		itemid=19244022
		commenturl='https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv25' % (itemid)
		l=ItemLoader(item=JiadianItem(), response=response)
		l.add_css('name','.sku-name::text', TakeFirst())
		# l.add_css('id','.follow::attr(data-id)', TakeFirst())
		# l.add_css('price','.price::text', TakeFirst())
		# l.add_css('brand','#parameter-brand a::text', TakeFirst())
		# l.add_css('parameter','.p-parameter-list li::text')
		# l.add_value('parameter','无')
		# l.add_css('summary_service','#summary-service span::text', TakeFirst())
		# l.add_css('add_service','#summary-support span::text')
		# l.add_value('add_service','无')
		# l.add_css('sales_promotion','.p-promotions em.hl_red::text')
		# l.add_value('sales_promotion','无')
		# l.add_css('store','.J-hove-wrap a::text', TakeFirst())
		# l.add_css('store_link','.J-hove-wrap a::attr(href)', TakeFirst())
		# l.add_css('commentsnum','.J-comments-list li[clstag*="allpingjia"]::attr(data-num)', TakeFirst())
		# l.add_css('goodcomments','.percent-con::text', TakeFirst())
		# l.add_css('goodcommentnum','.J-comments-list li[clstag*="haoping"]::attr(data-num)', TakeFirst())
		# l.add_css('comment_tags','.tag-list span::text')
		# l.add_css('mediumcommentnum','.J-comments-list li[clstag*="zhongping"]::attr(data-num)', TakeFirst())
		# l.add_css('badcommentnum','.J-comments-list li[clstag*="chaping"]::attr(data-num)', TakeFirst())
		# l.add_value('summary_service','无')
		# l.add_value('url',response.url)
		# l.add_value('price','0')
		# l.add_value('brand','范思哲（VERSACE）')
		# return l.load_item()
		yield scrapy.Request(commenturl,callback=self.parse_comments,meta={'item':l})
	def parse_comments(self,response):
			# print(response.body.decode('gbk').replace('fetchJSON_comment98vv25(','')[0:-2])
			l=response.meta['item']
			# print(item['name'])
			j=json.loads(response.body.decode('gbk').replace('fetchJSON_comment98vv25(','')[0:-2])['productCommentSummary']
			l.add_value('commentsnum',j['commentCount'])
			l.add_value('goodcomments',j['goodRateShow'])
			l.add_value('goodcommentnum',j['goodCount'])
			l.add_value('mediumcommentnum',j['generalCount'])
			l.add_value('badcommentnum',j['poorCount'])

			for key,value in j['productCommentSummary'].items():
				print("%s ---------- %s" % (key,value))

import scrapy
from scrapy_splash import SplashRequest
from scrapy.utils.response import open_in_browser
from myspider.items import JiadianItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
import scrapy_splash

class Myspider(scrapy.Spider):
	name='myspider'
	start_urls=["https://search.jd.com/search?keyword=%E8%8C%83%E6%80%9D%E5%93%B2&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E8%8C%83%E6%80%9D%E5%93%B2&cid2=2615&cid3=9188&page=1&s=274&click=0"]
	prourl="http://192.168.56.101:8050"
	def start_requests(self):
		for url in self.start_urls:
			script="""
			function main(splash)
				local url = splash.args.url
				assert(splash:go(url))
				assert(splash:wait(0.5))
				assert(splash:autoload("https://code.jquery.com/jquery-3.2.1.min.js"))
				local js = 'window.scrollBy(0,20000);$(".pn-next").trigger("click")'
				assert(splash:runjs(js))
				assert(splash:wait(1.5))
				return {
					html = splash:html(),
					a=splash:url(),
					nonext='0'
				}
			end
			"""
			yield SplashRequest(self.prourl,endpoint='execute',callback=self.parse,dont_filter=True,args={
				'url':url,'wait':0.5,'lua_source': script
				})

	def parse(self,response):
		items=response.css('.gl-item')
		# itemurls=response.css('#J_goodsList .p-name>a::attr(href)').extract()
		for item in items:
			url=item.css('.p-name>a::attr(href)').extract_first()
			price=item.css('.p-price i::text').extract_first()
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
			print('itemurl==============================')
			url=response.urljoin(url)
			yield SplashRequest(url,endpoint='execute',magic_response=True,callback=self.parse_item,dont_filter=True,slot_policy=scrapy_splash.SlotPolicy.SINGLE_SLOT,meta={'price':price},args={
			'url':url,'wait':2.5,'lua_source':itemscript,'timeout':50
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
			local js = '$(".pn-next").trigger("click")'
			assert(splash:runjs(js))
			local nonext=splash:evaljs('String($(".pn-next").hasClass("disabled"))')
			return {
				html = splash:html(),
				a=splash:url(),
				nonext=nonext
			}
		end
		"""
		# if nonext=="false":
		# 	yield SplashRequest(self.prourl,endpoint='execute',callback=self.parse,dont_filter=True,args={
		# 		'url':url,'wait':0.5,'lua_source': script
		# 		})
		
	def parse_item(self,response):
		with open('item1.html','w',encoding='utf-8-sig') as f:
			f.write(str(response.data['html']))
		print('startparseitem---------------------------------')
		print(response.real_url)
		print(response.css('.p-parameter-list *::text').extract())
		l=ItemLoader(item=JiadianItem(), response=response)
		l.add_css('name','.sku-name::text', TakeFirst())
		l.add_css('id','.follow::attr(data-id)', TakeFirst())
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
		l.add_css('store','strong a[clstag*="allpingjia"]::text', TakeFirst())
		l.add_css('store_link','strong a[clstag*="allpingjia"]::attr(href)', TakeFirst())
		l.add_css('commentsnum','.J-comments-list li[clstag*="allpingjia"]::attr(data-num)', TakeFirst())
		l.add_css('goodcomments','.percent-con::text', TakeFirst())
		l.add_css('goodcommentnum','.J-comments-list li[clstag*="haoping"]::attr(data-num)', TakeFirst())
		l.add_css('comment_tags','.tag-list span::text')
		l.add_css('mediumcommentnum','.J-comments-list li[clstag*="zhongping"]::attr(data-num)', TakeFirst())
		l.add_css('badcommentnum','.J-comments-list li[clstag*="chaping"]::attr(data-num)', TakeFirst())
		l.add_value('store','无')
		l.add_value('store_link','无')
		l.add_value('commentsnum','0')
		l.add_value('goodcomments','0')
		l.add_value('goodcommentnum','0')
		l.add_value('comment_tags','无')
		l.add_value('mediumcommentnum','0')
		l.add_value('badcommentnum','0')
		l.add_value('summary_service','无')
		l.add_value('url',response.url)
		l.add_value('price',response.meta['price'])
		l.add_value('brand','范思哲（VERSACE）')
		return l.load_item()


import scrapy
from scrapy_splash import SplashRequest
from myspider.items import YihaoList,YihaoItem
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
		splashjs="""
		function main(splash)
		  local url = splash.args.url
		  assert(splash:go(url))
		  assert(splash:wait(2.5))
		  local scroll_to = splash:jsfunc("window.scrollTo")
		   scroll_to(0, 30000)
		  assert(splash:wait(3.5))
		  return {
		    html = splash:html(),
		  }
		end
		"""
		for i in range(1,2):
			url='%s#page=%s&sort=1' % (response.url,i)
			print('----------')
			print(url)
			yield SplashRequest(url,callback=self.parse_list,args={'lua_source':splashjs,'url':url,'wait':2.5},dont_filter=True,endpoint='execute')

	def parse_list(self,response):
		alllists=response.css("#itemSearchList>div .proName>a")
		print("+++++++++++++++++++++++++++")
		for l in alllists:
			url=l.css("::attr('href')").extract_first()
			if(re.search('item',url)):
				url=response.urljoin(url)
				yield SplashRequest(url,callback=self.parse_item,args={'url':url,'wait':2.5},dont_filter=True)


	def parse_item(self,response):
		commenturl='http://e.yhd.com/front-pe/queryExpLabelSummary.do?productId=4281693'
		item=ItemLoader(item=YihaoItem(),response=response)
		image_url=response.urljoin(response.css(".proImg>img::attr('src')").extract_first())
		price="".join(response.css('#current_price *::text').extract())
		item.add_css('id','#mainProductId::attr("value")',TakeFirst())
		item.add_value("images_url",image_url)
		item.add_value("url",response.url)
		item.add_value('price',price)
		item.add_css('name','#productMainName::text',TakeFirst())
		item.add_css('parameter','.des_info>dd::text')
		item.add_css('summary_service','#detailDeliveryInfo>a::text',TakeFirst())
		item.add_value('summary_service','一号店')
		item.add_value('brand','无')
		item.add_value('price','无')
		item.add_value('images','无')
		item.add_value('sales_promotion','无')
		item.add_value('add_service','无')
		item.add_value('store_link','无')
		item.add_value('commentsnum','无')
		item.add_value('goodcomments','无')
		item.add_value('comment_tags','无')
		item.add_value('goodcommentnum','无')
		item.add_value('badcommentnum','无')
		item.add_value('mediumcommentnum','无')
		item.add_value('store','无')
		yield item.load_item()

	def parse_cats(self,response):
		allsorts=response.css(".alonesort .mc em a");
		item=YihaoItem()
		for l in allsorts:
			item['url']=response.urljoin(l.css("::attr('href')").extract_first())
			item['name']=l.css("::text").extract_first()
			print(item)
			yield item



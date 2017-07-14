import scrapy
from scrapy_splash import SplashRequest
from myspider.items import TaobaolistItem,JdItem,TaobaoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join
import re
import json

class TaobaoSpider(scrapy.Spider):
	name="taobaospider"

	pageoffset=60

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	cookies={"_tb_token_":"5b1483897cddf"}
	start_urls=['https://www.taobao.com/tbhome/page/market-list?spm=a21bo.7925171.191431.2.jascIR']

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url,callback=self.parse_cate,headers=self.headers,cookies=self.cookies,meta={'cookiejar': 1})

	def parse_cate(self,response):
		# lists=response.css('.category-name')
		# for l in lists:
		# 	item=TaobaolistItem()
		# 	name=l.css('::text').extract_first()
		# 	url=l.css('::attr(href)').extract_first()
		# 	url=response.urljoin(url)
		# 	item['name']=name
		# 	item['url']=url
		# 	yield item
			# if(re.search("s.taobao.com/list?q",url)):
		url=r'https://s.taobao.com/list?q=%E6%97%B6%E5%B0%9A%E5%A5%97%E8%A3%85&cat=50344007&style=grid&seller_type=taobao&spm=a219r.lm895.1000187.1'	
		for i in range(100):
			u='%s&s=%s' % (url,str(i*self.pageoffset))
			yield SplashRequest(u,callback=self.parse_list,headers=self.headers,meta={'cookiejar': response.meta['cookiejar']})

	def parse_list(self,response):
		s=re.search('g\_page\_config = .*\}\};',response.body.decode('utf-8'))
		itemjson=json.loads(s.group().replace("g_page_config = ","").replace("}};","}}"))
		listjson=itemjson['mods']['itemlist']['data']['auctions']

		for u in listjson:
			url=response.urljoin(u['detail_url'])

			yield scrapy.Request(url,callback=self.parse_item,headers=self.headers,meta={'cookiejar': response.meta['cookiejar']})


	def parse_item(self,response):
		url=response.url
		if(re.search('detail.tmall.com',url)):
			summary_service='天猫'
		else:
			summary_service='淘宝'
		l=ItemLoader(item=TaobaoItem(), response=response)
		l.add_value('url',url)
		l.add_css('id','#J_Pine::attr(data-itemid)',TakeFirst())
		l.add_css('sellerid','#J_Pine::attr(data-sellerid)',TakeFirst())
		l.add_css('shopid','#J_Pine::attr(data-shopid)',TakeFirst())
		l.add_css('name','.tb-main-title::text',TakeFirst())
		l.add_css('shopdesscore','.tb-shop-rate dl:nth-child(1) a::text',TakeFirst())
		l.add_css('shopservscore','.tb-shop-rate dl:nth-child(2) a::text',TakeFirst())
		l.add_css('shopdeliverscore','.tb-shop-rate dl:nth-child(3) a::text',TakeFirst())
		l.add_css('store','.tb-shop-name a::text',TakeFirst())
		l.add_css('store_link','.tb-shop-name a::attr(href)',TakeFirst())
		l.add_css('parameter','.attributes-list *::text')
		l.add_css('images_url','#J_ImgBooth::attr(src)',TakeFirst())
		l.add_value('images_url','无')
		l.add_value('parameter','无')
		l.add_value('summary_service',summary_service)
		l.add_value('sales_promotion',"无")
		l.add_value('add_service',"无")

		l.add_css('brand','.J_EbrandLogo::text',TakeFirst())
		l.add_value('brand','无')

		priceurl='https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&sellerId=%s&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,contract,tradeContract&callback=onSibRequestSuccess' % (response.css('#J_Pine::attr(data-itemid)').extract_first(),response.css('#J_Pine::attr(data-sellerid)').extract_first())

		itemid=response.css('#J_Pine::attr(data-itemid)').extract_first()
		userNumId=response.css('#J_Pine::attr(data-sellerid)').extract_first()
		yield scrapy.Request(priceurl,callback=self.parse_price,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36','referer':url},meta={'l':l,'url':url,'itemid':itemid,'userNumId':userNumId,'cookiejar': response.meta['cookiejar']})
	def parse_price(self,response):
		l=response.meta['l']
		print("++++++++++++++++++++++++++===")
		print(response.body.decode('UTF-8'))
		itemjson=json.loads(response.body.decode('UTF-8').replace("onSibRequestSuccess(","")[0:-2])
		print(itemjson)
		itemdata=itemjson['data']
		l.add_value('sendcity',itemdata['deliveryFee']['data']['sendCity'])
		try:
			l.add_value('price',itemdata['promotion']['promoData']['def'][0]['price'])
		except Exception:
			pass
		l.add_value('price','无')
		l.add_value('oriprice',itemdata['price'])
		l.add_value('soldtotalcount',itemdata['soldQuantity']['soldTotalCount'])
		commenturl="https://rate.taobao.com/detailCommon.htm?auctionNumId=%s&userNumId=%s" % (response.meta['itemid'],response.meta['userNumId']) + r"&ua=015UW5TcyMNYQwiAiwZTXFIdUh1SHJOe0BuOG4%3D%7CUm5Ockt%2FRX1Cf0J3Q35DeS8%3D%7CU2xMHDJ7G2AHYg8hAS8XLQMjDVEwVjpdI1l3IXc%3D%7CVGhXd1llXGhSalVoVWBVYVplUm9Nd05wSXJNd0xySX1Ee0N9Qmw6%7CVWldfS0QMAkwCCgSMhwgBC9PI0wqBFIE%7CVmJCbEIU%7CV2lJGSQEORklGyIWNg40DDgYJBohGjoAOw4uEiwXLAw2CTxqPA%3D%3D%7CWGFcYUF8XGNDf0Z6WmRcZkZ8R2dZDw%3D%3D&callback=json_tbc_rate_summary"
		yield scrapy.Request(commenturl,callback=self.parse_comment,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36','referer':response.meta['url']},meta={'l':l,'cookiejar': response.meta['cookiejar']}) 
		
	def parse_comment(self,response):

		print(response.body.decode('gbk').replace("json_tbc_rate_summary(","")[0:-1])
		itemjson=json.loads(response.body.decode('gbk').replace("json_tbc_rate_summary(","")[0:-1])

		l=response.meta['l']
		l.add_value('comments',itemjson['data']['count'])
		l.add_value('comment_tags',itemjson['data']['impress'])
		l.add_value('comment_tags',"无")
		return l.load_item()


			
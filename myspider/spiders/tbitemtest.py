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

class TaobaoItem(scrapy.Spider):
	name='tbitem'
	start_urls=['https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fspm%3Da219r.lm0.14.1.70b3a5556vRLHS%26id%3D544884387701%26ns%3D1%26abbucket%3D19']
	
	url=["https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=544884387701&sellerId=880436655&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess"]

	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	cookies={"_tb_token_":"5b1483897cddf","_nk_":"aiai20062079","cookie1":"Vv7BlTlDx9FiP1641p238yQ7xxLR%2BnKB0EcJezgG6Sw%3D","cookie17":"UUplZfavsamX","cookie2":"1c634bfc11a90c9a3366660b95690401","unb":"224462902","miid":"1451644460590886076","skt":"405b2acd0115be49"}

	def start_requests(self):
		for u in self.start_urls:
			yield scrapy.Request(u,callback=self.parse_item,headers=self.headers,meta={'cookiejar': 1},cookies=self.cookies)

	def parse_item(self,response):
		print(response.body)
		with open('tbitemtest.html','wb') as f:
			f.write(response.body)

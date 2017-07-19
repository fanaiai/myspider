# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Join

def rstrip_str(value):
	return str(value).replace('\n','').rstrip().lstrip()

def getnum(value):
	return value.replace('￥','')

class Join1(object):

	def __init__(self, separator=u' '):
		self.separator = separator

	def __call__(self, values):
		if(len(values)>1):
			return self.separator.join(values[:-1])
		elif(len(values)==1):
			return values[0]
		else:
			return '无'
class JdlistItem(scrapy.Item):
	url=scrapy.Field()
	name=scrapy.Field()

class TaobaolistItem(scrapy.Item):
	url=scrapy.Field()
	name=scrapy.Field()

class YihaoList(scrapy.Item):
	url=scrapy.Field()
	name=scrapy.Field()

class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JiadianItem(scrapy.Item):
	id=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	name=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	price=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	brand=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	parameter=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	images=scrapy.Field()
	images_urls=scrapy.Field()
	summary_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sales_promotion=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	add_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store_link=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcomments=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	commentsnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	mediumcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	badcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	comment_tags=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
class JdItem(scrapy.Item):
	id=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	name=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	price=scrapy.Field(input_processor=MapCompose(rstrip_str,getnum),output_processor=Join1())
	brand=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	parameter=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	images=scrapy.Field()
	images_url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	summary_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sales_promotion=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	add_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store_link=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcomments=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	commentsnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	mediumcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	badcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	comment_tags=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())

class YihaoItem(scrapy.Item):
	id=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	name=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	price=scrapy.Field(input_processor=MapCompose(rstrip_str,getnum),output_processor=Join1())
	brand=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	parameter=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	images=scrapy.Field()
	images_url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	summary_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sales_promotion=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	add_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store_link=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcomments=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	commentsnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	mediumcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	badcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	comment_tags=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())

class TaobaoItem(scrapy.Item):
	id=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	name=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	price=scrapy.Field(input_processor=MapCompose(rstrip_str,getnum),output_processor=Join1())
	brand=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	parameter=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	images=scrapy.Field()
	images_url=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	summary_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sales_promotion=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	add_service=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	store_link=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcomments=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	commentsnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	goodcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	mediumcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	badcommentnum=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	comment_tags=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sendcity=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	oriprice=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	soldtotalcount=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	sellerid=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	shopid=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	shopdesscore=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	shopservscore=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	shopdeliverscore=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())
	comments=scrapy.Field(input_processor=MapCompose(rstrip_str),output_processor=Join1())

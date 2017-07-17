# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import logging
from myspider.items import JdlistItem,JdItem,TaobaolistItem,TaobaoItem,YihaoItem

class InsertMysql(object):
	def open_spider(self,spider):
		self.conn=pymysql.connect(host='localhost',user='root',password='11111111',db='python',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
		self.cursor=self.conn.cursor()

	def close_spider(self,spider):
		self.cursor.close()
		self.conn.close()

	def process_item(self,item,spider):
		if isinstance(item,JdlistItem):
			self.cursor.execute('insert into jdlist(name,url) values("%s","%s")' % (item['name'],item['url']))
		elif isinstance(item,TaobaolistItem):
			self.cursor.execute('insert into taobaolist(name,url) values("%s","%s")' % (item['name'],item['url']))
		elif isinstance(item,YihaoItem):
			self.cursor.execute('insert into yihaolist(name,url) values("%s","%s")' % (item['name'],item['url']))
		elif isinstance(item,JdItem):
			self.cursor.execute('insert into jiadian(id,name,price,brand,parameter,summary_service,url,sales_promotion,add_service,store_link,commentsnum,goodcomments,comment_tags,goodcommentnum,mediumcommentnum,badcommentnum,store,images_url) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item['id'],item['name'],item['price'],item['brand'],item['parameter'],item['summary_service'],item['url'],item['sales_promotion'],item['add_service'],item['store_link'],item['commentsnum'],item['goodcomments'],item['comment_tags'],item['goodcommentnum'],item['mediumcommentnum'],item['badcommentnum'],item['store'],item['images_url']))
		elif isinstance(item,TaobaoItem):
			self.cursor.execute('insert into taobaoitem(id,name,price,brand,parameter,summary_service,url,sales_promotion,add_service,store_link,store,sendcity,oriprice,soldtotalcount,sellerid,shopid,shopdesscore,shopservscore,shopdeliverscore,comments,comment_tags,images_url) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item['id'],item['name'],item['price'],item['brand'],item['parameter'],item['summary_service'],item['url'],item['sales_promotion'],item['add_service'],item['store_link'],item['store'],item['sendcity'],item['oriprice'],item['soldtotalcount'],item['sellerid'],item['shopid'],item['shopdesscore'],item['shopservscore'],item['shopdeliverscore'],item['comments'],item['comment_tags'],item['images_url']))
		self.conn.commit()
		return item

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

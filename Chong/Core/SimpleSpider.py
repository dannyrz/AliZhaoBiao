# -*- coding: utf-8 -*-
# 这个类是一个简单的爬虫类，应该是抽象出一个爬虫最基本的功能，就是获取指定网页的html内容
from Core.Spider import Spider

class SimpleSpider(Spider):
	def readonly(self):
		return 1
	def request(self):
		a=1;

	def __init__(self,fields):
		self.fields=fields;
	 
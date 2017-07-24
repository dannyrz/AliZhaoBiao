# -*- coding: utf-8 -*-
# 这个类是一个简单的爬虫类，应该是抽象出一个爬虫最基本的功能，就是获取指定网页的html内容
from Core.Spider import Spider
import requests
import Core.Log
import logging


head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'} 


class SimpleSpider(Spider):

	def __init__(self,args):
		self.args=args;
	 
	def request(self,url,callback):
		response = requests.get(url,headers=head)

		logging.info("success send a request:"+url)

		content = response.content
		callback(self,url,content)

		return content
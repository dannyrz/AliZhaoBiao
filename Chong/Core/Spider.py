# -*- coding: utf-8 -*-
from abc import ABCMeta,abstractmethod,abstractproperty
from lxml import etree

class Spider(metaclass=ABCMeta):

	ID=0;

	def __init__(self,args):
		self.args=args;
 
	@abstractmethod
	def request(self,url,callback):
		pass

	# def parse(self,html):
	# 	fields=self.args['Fields'];
	# 	row={}
	# 	for key in fields:
	# 		row[key]=html.xpath(fields[key])[0].xpath('string(.)').strip()
	# 	return row


# -*- coding: utf-8 -*-
from abc import ABCMeta,abstractmethod,abstractproperty
from lxml import etree

class Spider(metaclass=ABCMeta):

	def __init__(self,fields):
		self.fields=fields;

	@abstractproperty
	def readonly(self):
		return self._x
 
	@abstractmethod
	def request(self):
		pass

	def parse(self,html):
		fields=list(self.fields);
		row={}
		for fieldName in fields:
			row[fieldName]=html.xpath(self.fields[fieldName])[0].xpath('string(.)').strip()
		print(row);
		return row


# -*- coding: utf-8 -*-
from abc import ABCMeta,abstractmethod,abstractproperty
from lxml import etree

class Spider(metaclass=ABCMeta):

	def __init__(self,task):
		self.task=task;

	@abstractproperty
	def readonly(self):
		return self._x
 
	@abstractmethod
	def request(self):
		pass

	def parse(self,html):
		fields=self.task['Fields'];
		row={}
		for key in fields:
			row[key]=html.xpath(fields[key])[0].xpath('string(.)').strip()
		return row


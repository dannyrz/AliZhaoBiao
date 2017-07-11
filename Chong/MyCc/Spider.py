# -*- coding: utf-8 -*-
import abc

class Spider(metaclass=abc.ABCMeta):  ##抽象类

	@abstractproperty
	def readonly(self):
  		return self._x
 
    @abc.abstractmethod  ##抽象方法
    def getContent(self):pass


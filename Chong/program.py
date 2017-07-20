# -*- coding: utf-8 -*-
# Chain.py是模块（Module），
# 在代码里定义的Class Chain是在模块里定义的类
# 一种方法是from Chain import Chain
# 还有一种方法是用 a =  Chain.Chain()
# 相当于从模块里索引出这个类两种方法都可以。
from Core.Spider import Spider
from Core.SimpleSpider import SimpleSpider
import requests
from lxml import etree
import pymysql.cursors
import time, os, sched 
import multiprocessing
import redis
import re
import json
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                filename='myapp.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

dbconn = {
    'host':'123.157.8.102',
    'port':3307,
    'user':'root',
    'passwd':'root',
    'db':'alizhaobiao',
    'charset':'utf8',
         }

pool = redis.ConnectionPool(host='112.12.79.58',db=0, port=6379,password='redis1997@lydong.com')
cache = redis.Redis(connection_pool=pool)


processDict={}


#此处的核心是要标记进程单次请求的页面列表不能重复请求，但同时为了增量更新，程序必须标注进程的记号。
def parse(spider,content):
	selector = etree.HTML(content)
	fields=spider.args['PagePropertyRegularExpression'];#页面提取属性
	for item in selector.xpath(spider.args['PageListRegularExpression']): #文章列表提取
		url=item.xpath(spider.args['PageURLRegularExpression'])[0] #基于列表开始的文章链接提取
		if url is  None:
			continue
		
		url=urljoin(url,url)
		if  cache.get(url) is None:
			link={
				'url':url,
				'task':spider.args
			}
			cache.rpush("link",json.dumps(link))
			cache.set(url,url)
		else:
			break
			

	for url in selector.xpath(spider.args['ListURLRegularExpression']):#分页链接提取
		key="PageList:"+str(Spider.ID)
		if(cache.get(key) is None):
			cache.set(key,url)
			spider.request(url, callback=parse)
		else:
			continue
		

def workSpider(task):
	starturl=task['StartURL'].split('\n') #入口页
	spider=SimpleSpider(task)
	Spider.ID+=1;
	for url in starturl:
		url=url.strip()
		if url!='':
			spider.request(url,callback=parse);
	time.sleep(20)

#该函数已经测试过创建出的进程会随机运行该函数，说明进程各司其职
def runTaskProcess(task):
	processName=task['SpiderName']
	process=multiprocessing.Process(target=workSpider,args=(task,))
	process.name=processName
	processDict[processName]=process;
	process.start()
	logging.info('start new process:%s' % processName)



def dispatchTaskProcess(task):
	processName=task['SpiderName']
	on=task['Status']==1;
	process= processDict.get(processName,False)
	if process==False:
		if on==True:
			runTaskProcess(task)
	else:
		if  process.is_alive()==False and on==True:
			print('task is not alived and sql config:on is true.')
			process.terminate()
			runTaskProcess(task)
		elif process.is_alive()==True and on==False:
			print('task is lived and sql config:on is false.')
			process.terminate()
		elif process.is_alive()==False and on==False:
			print('task is not alived and sql config:on is false.')
			process.terminate()
		elif process.is_alive()==True and on==True:
			print('task is alived and sql config:on is true. it is in running.')

def popTask():
	while True:
		connect = pymysql.Connect(**dbconn) # 连接数据库
		cursor = connect.cursor() # 获取游标
		sql = "SELECT * FROM chong_task"
		cursor.execute(sql)
		task={}
		index = cursor.description
		result = []
		for res in cursor.fetchall():
			row = {}
			for i in range(len(index)):
				row[index[i][0]] = res[i]
			yield row
		cursor.close()
		connect.close()

		time.sleep(10)

def scanTask():
	for row in popTask():
		dispatchTaskProcess(row)
		# for row in cursor.fetchall():
		# 	task["IID"]=row[1];
		# 	task["Name"]=row[2];
		# 	task["Charset"]=row[3];
		# 	task["InURLRegularExpression"]=row[4];
		# 	task["InURLNumber"]=row[5];
		# 	task["PageProperty"]=row[6];
		# 	task["PagePropertyRegularExpression"]=row[7];
		# 	task["BodyFilterTextRegularExpression"]=row[8];
		# 	task["TextReplace"]=row[9];
		# 	task["WorkInterval"]=row[10];
		# 	task["ThreadNumber"]=row[11];
		# 	task["DatabaseConnectStr"]=row[12];
		# 	task["Status"]=row[13];
		# 	task["EnableBroswer"]=row[14];
		# 	task["ResponseFormat"]=row[15];
		# 	task["Account"]=row[16];
		# 	task["NeedLogin"]=row[17];
		# 	task["SpiderName"]=row[18];

def parsePage(spider,html):
	selector = etree.HTML(html)
	html=html.decode('utf-8')
	propertys=json.loads(spider.args['PagePropertyRegularExpression'])
	for key in propertys:
		
		item=propertys[key];
		if item.startswith('$'):
			p1 = r'%s' % item[1:]
			pattern = re.compile(p1)
			match = pattern.search(html)
 
			if match:
				propertys[key]=match.group(1)
			#对文章的内容进行特殊处理，提取图片
			if key=='content_raw' and spider.args['DownLoadImg']==1:
				imgselector=etree.HTML(propertys[key])
				for imgsrc in imgselector.xpath("//img/@src"):
					if imgsrc is not None and len(imgsrc)>0:
						cache.rpush('link-img',imgsrc)
						logging.info('push a img link to queue %s .' %imgsrc)


		else:
			item=selector.xpath(item)[0]
			propertys[key]=item

	print(propertys)
	

	
def startQueueSpider():
	while True:
		link=cache.lpop("link")
		if link is None:
			logging.warning('none link in queue, waiting 10s try to get again.')
			time.sleep(10)
			continue
		linkDict=json.loads(link.decode('utf-8'))
		url=linkDict['url']
		args=json.loads(json.dumps(linkDict['task']))
		spider=SimpleSpider(args)
		spider.request(url, callback=parsePage)

		time.sleep(5)
		


if __name__ == '__main__':
	startQueueSpider()
	#scanTask()
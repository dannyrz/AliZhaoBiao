# -*- coding: utf-8 -*-
# Chain.py是模块（Module），
# 在代码里定义的Class Chain是在模块里定义的类
# 一种方法是from Chain import Chain
# 还有一种方法是用 a =  Chain.Chain()
# 相当于从模块里索引出这个类两种方法都可以。
from Core.Spider import Spider
from Core.SimpleSpider import SimpleSpider
import logging
import Core.Log 
import requests
from lxml import etree
import pymysql.cursors
import time, os, sched 
import multiprocessing
import redis
import re
import json
from urllib.parse import urljoin
from urllib.parse import splittype
from urllib.parse import splithost
from urllib.parse import urlparse
from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies
import os

logging.basicConfig(level=logging.DEBUG,
     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            filename='log.log',
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


#判断同一进程运行时分页连接是否已抓取过
def isspided(spiderid,url):
	key="PageList-%s:%s" %(str(Spider.ID),str(hash(url)))
	spided = cache.get(key)
	if spided is None:
		return False
	else:
		return True

def markspided(spiderid,url):
	key="PageList-%s:%s" %(str(Spider.ID),str(hash(url)))
	cache.set(key,url)


#此处的核心是要标记进程单次请求的页面列表不能重复请求，但同时为了增量更新，程序必须标注进程的记号。
def parse(spider,url,response):
	content=response.content
	logging.info('callback pagelist-parse url: %s' % url)

	selector = etree.HTML(content)
	fields=spider.args['PagePropertyRegularExpression'];#页面提取属性
	for item in selector.xpath(spider.args['PageListRegularExpression']): #文章列表提取
		itemurl=item.xpath(spider.args['PageURLRegularExpression'])[0] #基于列表开始的文章链接提取
		if itemurl is  None:
			continue
		
		itemurl=urljoin(url,itemurl)
		if  cache.get(itemurl) is None:
			link={
				'url':itemurl,
				'task':spider.args
			}
			cache.rpush("link",json.dumps(link))
			cache.set(itemurl,itemurl)

			logging.info('successfully fetch a item and push to redis list url: %s' %itemurl)
		else:
			logging.info('page list,s item has finished fetch: %s' %itemurl)
			break

	markspided(spider.ID,url)

	logging.info('finished parse item list link .')

	for url in selector.xpath(spider.args['ListURLRegularExpression']):#分页链接提取
		if isspided(Spider.ID,url)==False:
			spider.request(url, callback=parse)
		else:
			logging.info('list page url:%s has been fectked .' % url)
			continue
		

def workSpider(task):
	starturl=task['StartURL'].split('\n') #入口页
	spider=SimpleSpider(task)
	for url in starturl:
		url=url.strip()
		if url!='':
			spider.request(url,callback=parse);
	time.sleep(20)

#该函数已经测试过创建出的进程会随机运行该函数，说明进程各司其职
def runTaskProcess(task):
	process=multiprocessing.Process(target=workSpider,args=(task,))
	processName=task['SpiderName']
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
			logging.info('task is not alived and sql config:on is true.')
			process.terminate()
			runTaskProcess(task)
		elif process.is_alive()==True and on==False:
			logging.info('task is lived and sql config:on is false.')
			process.terminate()
		elif process.is_alive()==False and on==False:
			logging.info('task is not alived and sql config:on is false.')
			process.terminate()
		elif process.is_alive()==True and on==True:
			logging.info('task is alived and sql config:on is true. it is in running.')

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

def parsePage(spider,url,response):
	html=response.content
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
			if key=='content_raw':
				contentselector=etree.HTML(propertys[key])
				etree.strip_elements(contentselector, 'script')
				etree.strip_tags(contentselector, 'a')
				propertys[key]=etree.tostring(contentselector).decode('utf-8')
				if spider.args['DownLoadImg']==1:
					for imgsrc in contentselector.xpath("//img/@src"):
						if imgsrc is not None and len(imgsrc)>0:
							cache.rpush('link-img',imgsrc)
							proto, rest = splittype(imgsrc)
							res, rest = splithost(rest)
							propertys[key]=propertys[key].replace(imgsrc,imgsrc.replace(res,'img.zyai.top'))
							logging.info('push a img link to queue %s .' %imgsrc)


		else:
			item=selector.xpath(item)[0]
			propertys[key]=item

	dataPersistenceType=spider.args['DataPersistenceType']

	if dataPersistenceType=='WPRPC' :
		wp = Client('http://tech.cocopass.com/xmlrpc.php', 'admin', '19841204')

		"""
		发表博文
		"""
		post = WordPressPost()
		post.title = propertys['title'].encode('utf-8')
		post.content = propertys['content_raw'].encode('utf-8')
		post.post_status = 'publish'
		post.terms_names = {
			'post_tag': [post.title],
			'category': ['爱好']
		}
		wp.call(NewPost(post))
		logging.info('successfully post one article: %s .' % propertys['title'] )

	elif dataPersistenceType=='MYSQL':
		pass

	
def parseImage(spider,url,response):
	content=response.content
	filepathname =  "download%s"%urlparse(url).path
	path, filename = os.path.split(filepathname);
	if not os.path.exists(path):
		os.makedirs(path)
	open(filepathname, 'wb').write(content)

	logging.info('successfully down a image:%s' % filepathname)
	
def startQueueSpider(args):
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

def startImageQueueSpider(args):
	while True:
		link = cache.lpop("link-img")
		if link is None:
			logging.warning('none image link in queue, waiting 10s try to get again.')
			time.sleep(10)
			continue

		url = link.decode('utf-8')
		spider = SimpleSpider(None)
		spider.request(url, callback=parseImage)
		time.sleep(2)


def runPageSpider():
	process=multiprocessing.Process(target=startQueueSpider,args=(None,))
	process.start()
	logging.info('start new process: pageSpider .')




def runImageSpider():
	process = multiprocessing.Process(target=startImageQueueSpider, args=(None,))
	process.start()
	logging.info('start new process: ImageQueueSpider .')

if __name__ == '__main__':
	logging.info('program start.')
	#runImageSpider();
	runPageSpider()
	#scanTask()
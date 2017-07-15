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

dbconn = {
    'host':'123.157.8.102',
    'port':3307,
    'user':'root',
    'passwd':'root',
    'db':'alizhaobiao',
    'charset':'utf8',
         }

processDict={}


def parse(spider,content):
	selector = etree.HTML(content)
	fields=spider.args['Fields'];
	for url in selector.xpath(fields['PageURL']):
		print(url)
		spider.request(url, callback=parse)

	# row={}
	# for key in fields:
	# 	#row[key]=html.xpath(fields[key])[0].xpath('string(.)').strip()
	# 	row[key]=html.xpath(fields[key]);
	# print(row)
	# return row
			
			

def workSpider(task):
	starturl=task['StartURL'].split('\n')
	fields={
				"PageURL":"//div[@class='page']/a/@href"
			}
	args={
			'Fields':fields,
		}
	spider=SimpleSpider(args)
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
		
	

 



if __name__ == '__main__':
	scanTask()
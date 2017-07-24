# -*- coding: utf-8 -*-
from urllib.request import url2pathname
from urllib.parse import urljoin
from urllib.parse import urlparse
import os

url="https://www.china.com/imagd/dd/dd/e/kl/il.jpg"
r = urlparse(url)
filepathname =  "download/%s"%urlparse(url).path
p,f=os.path.split(filepathname);
if not os.path.exists(p):
	os.makedirs(p)
print (r.path)


url=urljoin("http://www.asite.com/folder/currentpage.html", "../www.asite.com/folder/anotherpage.html") 
print(url)


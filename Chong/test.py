# -*- coding: utf-8 -*-
from urllib.parse import urljoin


url=urljoin("http://www.asite.com/folder/currentpage.html", "../www.asite.com/folder/anotherpage.html") 
print(url)
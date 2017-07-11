# -*- coding: utf-8 -*-
# 这是有一个爬虫学习时的文件，抄自官方文档

import scrapy

class QuotesSpider(scrapy.Spider):
	
    name = "a" # 采用命令 scrapy crawl [name]运行时，与类名和文件名无关，与此处的爬虫名字有关

    def start_requests(self):
        urls = [
            'https://docs.scrapy.org/en/latest/intro/overview.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log(response.body)

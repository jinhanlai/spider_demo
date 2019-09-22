# -*- coding: utf-8 -*-
import scrapy


# 如果想要爬虫一开始的时候就post请求，用重写start_requests()方法
# post方法必须用scrapy.FormREquest()
class RerenSpiderSpider(scrapy.Spider):
    name = 'reren_spider'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"
        data = {
            'email': "15208213211",
            'password': "lailai5201314"
        }
        request = scrapy.FormRequest(url=url, formdata=data, callback=self.parse_page)
        yield request

    def parse_page(self, response):
        request = scrapy.FormRequest(url="http://www.renren.com/972069634/profile", callback=self.parse_profile)
        yield request

    def parse_profile(self, response):
        with open('reren.html', 'w', encoding='utf-8') as fp:
            fp.write(response.text)
        print('加载成功')

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class UserAgentDownloadMiddleware(object):
    pass

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"D:\ProgrameApp\chromedriver\chromedriver.exe")

    def process_request(self, request, spider):
        # request.headers['User-Agent']=""#这个可以修改User-Agent，可以设置成随机请求头
        self.driver.get(request.url)
        time.sleep(0.5)
        try:
            while True:
                showmore = self.driver.find_element_by_class_name('show-more')
                showmore.click()
                time.sleep(0.3)
                if not showmore:
                    break
        except:
            pass
        source = self.driver.page_source
        # 封装成response对象返回给爬虫
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request,encoding='utf-8')
        return response

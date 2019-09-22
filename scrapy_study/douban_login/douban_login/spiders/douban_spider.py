# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/passport/login']
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    home_url="https://douban.com"
    profile_url='https://www.douban.com/people/203932097/'
    edit_url="https://www.douban.com/j/people/203932097/edit_signature"
    def parse(self, response):
        formdata = {
            'ck': '3cp7',
            'name': '15208213211',
            'password': 'lailai5201314',
            'remember': 'true',
            'ticket': '',
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_next)

    def parse_next(self, response):
        yield scrapy.FormRequest(url=self.home_url, callback=self.parse_after_login)

    def parse_after_login(self, response):
        user=response.xpath("//li[@class='nav-user-account']/a/span/text()").get()
        if user:
            yield scrapy.FormRequest(url=self.profile_url,callback=self.parse_profile)
            print('用户{}登录成功！'.format(user))
        else:
            print('登陆失败')
    def parse_profile(self,response):
        if response.url==self.profile_url:
            # input=response.xpath("//input[@name='signature']/@value").get()
            formdata={
                'ck':"3cp7",
                'signature': 'hello,world'
            }
            yield scrapy.FormRequest(url=self.edit_url,formdata=formdata,callback=self.parse_none)
        else:
            print("没有进入到个人中心")

    def parse_none(self,response):
        pass

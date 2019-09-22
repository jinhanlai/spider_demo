# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZhipinSpiderSpider(CrawlSpider):
    name = 'zhipin_spider'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101270100/?query=python&page=1']

    rules = (
        #匹配职位列表的信息
        Rule(LinkExtractor(allow=r'.+/c101270100/?query=python&page=\d'),follow=True),
        #匹配职位详情页的信息
        Rule(LinkExtractor(allow=r'.+job_detail/.+'),callback="parse_job", follow=False),
    )

    def parse_job(self, response):
        print(response.text)
        title=response.xpath("//div[@class='name']/h1/text()").get().strip()
        salary=response.xpath("//div[@class='name']/span/text()").get().strip()
















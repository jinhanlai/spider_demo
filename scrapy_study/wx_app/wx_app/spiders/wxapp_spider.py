# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_study.wx_app.wx_app.items import WxAppItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'),
             follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),
             callback="parse_detail",follow=False)
    )

    def parse_detail(self, response):
        title=response.xpath("//h1[@class='ph']/text()").get()
        author=response.xpath("//p[@class='authors']/a/text()").get()
        time = response.xpath("//p[@class='authors']/span/text()").get()
        print('='*30)
        print(title,author,time)
        item=WxAppItem(title=title,author=author,time=time)
        yield item

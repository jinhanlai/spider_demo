# -*- coding: utf-8 -*-
import scrapy

from scrapy_study.qsbk_scripy.qsbk_scripy.items import QsbkScripyItem


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://qiushibaike.com/text/page/1/']
    base_domain = "http://qiushibaike.com"

    # i=0
    def parse(self, response):
        # SelectorList类型
        content = response.xpath("//div[@id='content-left']/div")
        print(content)
        # itemArray = []
        for ct in content:
            # SelectorList类型,要用get()获得第一个元素
            author = ct.xpath(".//h2/text()").get().strip()
            duanzhi = ct.xpath(".//div[@class='content']//text()").getall()
            duanzhi = "".join(duanzhi).strip()  # 把list对象拼接成字符串
            # 把信息提交给引擎，然后引擎吧消息给pipelines
            # infor={
            #     'author':author,
            #     'duanzhi':duanzhi
            # }

            infor = QsbkScripyItem(author=author, duanzhi=duanzhi)
            yield infor
            # #或者收集好所有的item然后返回，也是一样的
            # itemArray.append(infor)
            # return itemArray
        # self.i+=1
        # print(self.i)
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        # print(next_url)
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)

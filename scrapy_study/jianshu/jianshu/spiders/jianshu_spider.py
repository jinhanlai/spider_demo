# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_study.jianshu.jianshu.items import JianshuItem


class JianshuSpiderSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[a-z0-9]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        # 这是用ajax加载出来的，xpath找不到，必须配合selenium使用
        head_portrait = response.xpath("//img[@class='_3T9iJQ']/@src").get()
        author = response.xpath("//span[@class='_2vh4fr']/a/text()").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        article_id = response.url.split("?")[0].split('/')[-1]
        content = response.xpath("//article[@class='_2rhmJa']").get()
        # read_count = response.xpath("//article[@class='_2rhmJa']").get()
        # word_count = scrapy.Field()
        like_count = response.xpath("//span[@class='_3tCVn5']/span/text()").get()
        subject = ",".join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())
        item = JianshuItem(
            title=title,
            author=author,
            pub_time=pub_time,
            article_id=article_id,
            content=content,
            head_portrait=head_portrait,
            origin_urls=response.url,
            like_count=like_count,
            subject=subject,
        )
        yield item

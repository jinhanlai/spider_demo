# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    title=scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    article_id = scrapy.Field()
    head_portrait = scrapy.Field()
    content = scrapy.Field()
    origin_urls=scrapy.Field()
    read_count=scrapy.Field()
    word_count=scrapy.Field()
    like_count=scrapy.Field()
    subject=scrapy.Field()



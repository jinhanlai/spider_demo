# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    provice = scrapy.Field()  # 房子所在省份
    city = scrapy.Field()  # 房子所在城市
    name = scrapy.Field()  # 房子名字
    price = scrapy.Field()  # 房子价格
    house_type = scrapy.Field()  # 房屋类型(三居)
    area = scrapy.Field()  # 房子面积
    address = scrapy.Field()  # 房子所在地址
    district = scrapy.Field()  # 房子所在区域
    sale = scrapy.Field()  # 房子出售状态
    origin_url = scrapy.Field()  # 房子连接


class ESFHouseItem(scrapy.Item):
    provice = scrapy.Field()  # 房子所在省份
    city = scrapy.Field()  # 房子所在城市
    name = scrapy.Field()  # 房子名字
    price = scrapy.Field()  # 房子总价
    unit=scrapy.Field()#房屋单价
    house_type = scrapy.Field()  # 房屋类型(几室几厅)
    floor=scrapy.Field()#楼层
    toward=scrapy.Field()#朝向
    year=scrapy.Field()#年代
    area = scrapy.Field()  # 房子面积
    address = scrapy.Field()  # 房子所在地址
    district = scrapy.Field()  # 房子所在区域
    # master=scrapy.Field()
    # sale = scrapy.Field()  # 房子出售状态
    origin_url = scrapy.Field()  # 房子连接

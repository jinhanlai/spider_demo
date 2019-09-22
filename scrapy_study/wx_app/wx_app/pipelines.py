# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# from scrapy.exporters import JsonLinesItemExporter
#
#
# class WxAppPipeline(object):
#     def __init__(self):
#         self.fp = open('wxjc.json', 'wb')
#         self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def open_spider(self, spider):
#         print("开始")
#
#     def close_spider(self, spider):
#         print("关闭文件")
#         self.fp.close()


import json


class WxAppPipeline(object):
    def __init__(self):
        self.fp = open("wxjc.json", 'w', encoding='utf-8')
        # self.fp.write('HELLO')

    def process_item(self, item, spider):
        it_json = json.dumps(dict(item), ensure_ascii=False)  # 不该为False，会写入ascii值
        self.fp.write(it_json + '\n')
        print("write")
        return item

    def open_spider(self, spider):
        print("爬虫开始")

    def close_spider(self, spider):
        self.fp.close()
        print("爬虫结束")

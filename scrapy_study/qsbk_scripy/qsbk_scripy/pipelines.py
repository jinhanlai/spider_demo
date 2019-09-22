# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
class QsbkScripyPipeline(object):
    def __init__(self):
        self.fp=open("duanzhi.json",'w',encoding='utf-8')

    def process_item(self, item, spider):
        it_json=json.dumps(dict(item),ensure_ascii=False)#不该为False，会写入ascii值
        self.fp.write(it_json+'\n')

        return item

    def open_spider(self,spider):
        print("爬虫开始")

    def close_spider(self,spider):
        self.fp.close()
        print("爬虫结束")

# #这是读一行写一行，不占内存资源，但是写入的不是json格式
# from scrapy.exporters import JsonLinesItemExporter
# class QsbkScripyPipeline(object):
#     def __init__(self):
#         self.fp=open("duanzhi.json",'wb')
#         self.exporter=JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#
#
#     def process_item(self, item, spider):
#         # self.exporter.export_item("ASD")
#         self.exporter.export_item(item)
#         return item
#
#     def open_spider(self,spider):
#         print("爬虫开始")
#
#     def close_spider(self,spider):
#
#         self.fp.close()
#         print("爬虫结束")

#
# #这个是把数据暂存内存中，然后一次性写入，写入的是json格式，但是占内存资源
# from scrapy.exporters import JsonItemExporter
# class QsbkScripyPipeline(object):
#     def __init__(self):
#         self.fp=open("duanzhi.json",'wb')
#         self.exporter=JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
#         self.exporter.start_exporting()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def open_spider(self,spider):
#         print("爬虫开始")
#
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()
#         self.fp.close()
#         print("爬虫结束")
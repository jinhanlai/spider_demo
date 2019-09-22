# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from scrapy_study.fang.fang.items import NewHouseItem,ESFHouseItem
class FangPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'wb')
        self.oldhouse_fp = open('oldhouse.json', 'wb')
        self.newhouse_exporter=JsonLinesItemExporter(self.newhouse_fp,ensure_ascii=False)
        self.oldhouse_exporter = JsonLinesItemExporter(self.oldhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item,NewHouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item,ESFHouseItem):
            self.oldhouse_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.newhouse_fp.close()
        self.oldhouse_fp.close()
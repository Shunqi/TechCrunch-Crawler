# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


class TechspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('tech_article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "image_url" in item:
            for _, details in results:
                image_file_path = details["path"]
            item["image_path"] = image_file_path
        return item

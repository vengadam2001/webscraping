# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
# from scrapy.exceptions import DropItem
# from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
# from scrapy.http.request import Request
# import os
# from urllib.parse import urlparse
# from scrapy.exceptions import DropItem
import scrapy
# import os
# from urllib.parse import urlparse

# from scrapy.pipelines.files import FilesPipeline

# class MyFilesPipeline(FilesPipeline):

#     def file_path(self, request, response=None, info=None, *, item=None):
#         return 'files/' + os.path.basename(urlparse(request.url).path)

# from scrapy import settings
class DemoDownloaderPipeline:
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):
    def __init__(self):
        self.file = open("./torrents/college123.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
        
class MongoPipeline:
    collection_name = 'torrents'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item))
        return item
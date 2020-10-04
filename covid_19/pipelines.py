# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Item
import pymongo

class BaseDataPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'covid19_info_data')
        cls.collection_name = crawler.settings.get('MONGO_COLLECTION_NAME','news')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        collection = self.db[self.collection_name]
        dict_item = dict(item) if isinstance(item, Item) else item
        collection.insert(dict_item)
        return item

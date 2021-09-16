from itemadapter import ItemAdapter
from pymongo import MongoClient

class InstaPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.insta


    def process_item(self, item, spider):
        colection = self.mongo_base[item.get('username')]
        colection.insert_one(item)
        return item

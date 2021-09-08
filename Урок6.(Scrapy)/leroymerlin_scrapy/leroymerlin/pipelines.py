from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import hashlib
from scrapy.utils.python import to_bytes


class LeroymerlinPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.Leroymerlin



    def process_item(self, item, spider):
        print(spider.name)
        colection = self.mongo_base[spider.name]
        colection.insert_one(item)
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if
                          itm[0]]
        return item


    def file_path(self, request, response=None, info=None, *, item=None):    # реализация сохранения фото по папкам относительно URL
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        name = item['name']
        return f'full/{name}/{image_guid}.jpg'
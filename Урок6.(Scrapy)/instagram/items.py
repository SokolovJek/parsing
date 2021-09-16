# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from itemloaders.processors import MapCompose


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()  # TakeFirst()- берет первый элемент со списка
    username = scrapy.Field()  # MapCompose()-похоже на  функцию map()-обрабатует список
    photos = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    pass

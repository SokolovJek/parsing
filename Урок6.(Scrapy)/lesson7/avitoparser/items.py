# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst        # это класс обработчикjd;            # TakeFirst-это постобработчик(пред передачей item-ов в pipline), ПРЕДОБРАБОТЧИКИ-раьотают в момент сборки данных
from itemloaders.processors import MapCompose                                       # MapCompose- ПРЕДОБРАБОТЧИКИ-раьотают в момент сборки


def process_price(value):                                           # Функция для обработки цен
    value = value.replace('\xa0', '')
    try:
        return int(value)
    except:
        return value


"""реализацию обработки item-ов лутше делать здесь"""
class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())                                       #TakeFirst()- берет первый элемент со списка
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())     #MapCompose()-похоже на  функцию map()-обрабатует список
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    pass  #   ?
import scrapy
from itemloaders.processors import TakeFirst
from itemloaders.processors import MapCompose

def process_price(value):
    value = value.replace('\xa0', '')
    try:
        return float(value)
    except:
        return value

def descriptions(value):                                                # фунуция преобразование ОПИСАНИЯ в нормальный вид
    a = value
    f = a.replace('\n', '')
    g = f.strip(' ')
    if len(g) != 0:
        return g

class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    descriptions = scrapy.Field(input_processor=MapCompose(descriptions))    # создаем описание товара
    photos = scrapy.Field(input_processor=MapCompose())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    pass
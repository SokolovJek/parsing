# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
'''это КЛАСС item    здесь необхадимо ?'''

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    curs = scrapy.Field()
    _id = scrapy.Field()
    pass

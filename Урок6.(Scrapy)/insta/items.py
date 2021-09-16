import scrapy


class InstaItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    subscribers = scrapy.Field()
    subscriptions = scrapy.Field()
    pass

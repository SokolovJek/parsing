import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_scrapy.leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query,
                 **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://volgograd.leroymerlin.ru/search/?q={query}']

    def parse(self, response):
        ads_links = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]')
        for link in ads_links:
            yield response.follow(link,
                            callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(),
                            response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price',
                         "//meta[@itemprop='price']/@content")
        loader.add_xpath('photos', "//img/@data-origin")
        loader.add_xpath('descriptions', '//uc-pdp-section-layout//dl//text()')
        loader.add_value('url', response.url)
        yield loader.load_item()


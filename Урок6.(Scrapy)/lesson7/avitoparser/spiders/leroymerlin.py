import scrapy


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://volgograd.leroymerlin.ru/search/?q=%D0%B4%D0%B2%D0%B5%D1%80%D0%B8']




    def __init__(self, query,
                 **kwargs):  # lesson7 'создали конструкто для класа все это нужно чтоб передавать аргумент при поиске(ПР: ...?q=Land+Cruiser)
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.avito.ru/rossiya?q={query}']  # передаем аргумент

    def parse(self, response):
        '''Получаем ссылки на объекты и ссылку на след. страницу. НЕ вызываем(уходим от этого) метод getall и get как в УРОКЕ6 мы будем разгружать паука'''

        ads_links = response.xpath("//a[@data-marker='item-title']")
        for link in ads_links:
            yield response.follow(link,
                                  callback=self.parse_ads)  # получается так что scrapy сам обнаружет сылку, при условии что в теге <a> она ЕСТЬ!?

    def parse_ads(self, response: HtmlResponse):  # response это объект класса  HtmlResponse
        '''здесь паук уже не будет работать'''
        loader = ItemLoader(item=AvitoparserItem(),
                            response=response)  # Создаем отдельный объект для работы с item (здесь инициализируются все поля item'a и их обработчики)
        loader.add_xpath('name', "//h1/span/text()")  # Наполняем item данными (также сразу запускаются предобработчики)
        loader.add_xpath('price',
                         "//span[@class='js-item-price']/text()")  # указуеим сначала имя(как будет называтся в БД) а потом уже сам xpath
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-frame')]/@data-url")
        loader.add_value('url', response.url)  # просто добавляет наше значение в item
        yield loader.load_item()  # Отправляем в pipline (также здесь запускаются постобработчики)
        # loader.add_css()                                                              # если бы мы работали с css

"""этот код реализует команду (scrapy crawl avito)"""


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson7.avitoparser import settings
from lesson7.avitoparser.spiders.avito import AvitoSpider

if __name__ == '__main__':

    crawler_settings = Settings()                                       #здесь хранятся настройки
    crawler_settings.setmodule(settings)                                #setmodule - модуль который реализует парсинг нашего докуента settings и создает словарь с настройками

    process = CrawlerProcess(settings=crawler_settings)                 #создаем процесс и передаем настройки в атрибут
    # query = input('')                                             #при желании можно передавать значение( А ЛУТШЕ ВСЕГо передавать этот атрибут через sys метод argv)
    process.crawl(AvitoSpider, query='квартиры')                                           # в метод crawl передаем класс (lesson7и атрибут для поиска)!!!
    # process.crawl(LeroymerlinSpider, query='двери')
    process.start()



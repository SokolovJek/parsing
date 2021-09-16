"""этот код реализует команду (scrapy crawl avito)"""


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram import settings
from instagram.spiders.instagram import InstagramSpider

if __name__ == '__main__':

    crawler_settings = Settings()                                       #здесь хранятся настройки
    crawler_settings.setmodule(settings)                                #setmodule - модуль который реализует парсинг нашего докуента settings и создает словарь с настройками

    process = CrawlerProcess(settings=crawler_settings)                 #создаем процесс и передаем настройки в атрибут
    process.crawl(InstagramSpider)                                           # в метод crawl передаем класс (lesson7и атрибут для поиска)!!!

    process.start()



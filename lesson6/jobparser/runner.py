"""этот код реализует команду (scrapy crawl hhru)"""


from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider

if __name__ == '__main__':

    crawler_settings = Settings()                                       #здесь хранятся настройки
    crawler_settings.setmodule(settings)                                #setmodule - модуль который реализует парсинг нашего докуента settings и создает словарь с настройками

    process = CrawlerProcess(settings=crawler_settings)                 #создаем процесс и передаем настройки в атрибут
    process.crawl(HhruSpider)                                           # в метод crawl передаем класс
    process.crawl(SuperjobSpider)

    process.start()

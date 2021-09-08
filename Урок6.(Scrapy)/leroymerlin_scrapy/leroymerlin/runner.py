from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from leroymerlin_scrapy.leroymerlin import settings
from leroymerlin_scrapy.leroymerlin.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('')
    process.crawl(LeroymerlinSpider, query='двери')
    process.start()



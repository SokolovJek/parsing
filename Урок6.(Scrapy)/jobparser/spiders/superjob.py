import scrapy
from scrapy.http import HtmlResponse                                                    #импортируем класс объекта response
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        print()
        links = response.xpath('//a[contains(@class,"icMQ_ _6AfZ9")]/@href').getall()  # передаем данные с HTML кода(сылка на каждую вакансию).Метод getall нужен для сбора всей информации и создания словаря
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _1SCYW f-test-button-dalshe f-test-link-Dalshe"]//@href').get()  # переход на следуюющюю страницу(метод get он берет первый элемент со списка)

        print()
        if next_page:                                                                   # если список не пустой(в нем чтото есть )то переходи на слудуюющюю страницу
            yield response.follow(next_page, callback=self.parse)                       # yeild делает это один раз
        for link in links:                                                              # yield - нужен для поочередного обхода каждой сылки
            yield response.follow(link, callback=self.parse_vacancy)                    # callback -  это асинхронная функция,к которой обращается response после получения сылки
    def parse_vacancy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath('//span[@class="_1h3Zg _2Wp8I _2rfUm _2hCDz"]/text()').getall()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)

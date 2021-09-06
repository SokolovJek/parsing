import scrapy
from scrapy.http import HtmlResponse  #импортируем класс объекта response
from jobparser.items import JobparserItem
"""создаем парсер для сбора вакансий, он будет заходить на каждую страницу вакансии( по сылке) и собирать данные """

class HhruSpider(scrapy.Spider):
    name = 'hhru'                                                                               #имя паука
    allowed_domains = ['hh.ru']                                                                 #перечень доменов где он будет собирать
    start_urls = [
        'https://volgograd.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post&area=1',
        'https://volgograd.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post&area=2']  # точка входа(сылки или сылка)

    def parse(self, response: HtmlResponse):                                                    #указыаем явно класс объекта response(HtmlResponse) чтоб появлялись подсказки
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()    #передаем данные с HTML кода(сылка на каждую вакансию).Метод getall нужен для сбора всей информации и создания словаря
    # links = response.css() #можно и через него но нужно читать литературу(она будет достуна далее)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()                    #переход на следуюющюю страницу(метод get он берет первый элемент со списка)
        if next_page:                                                                           #если список не пустой(в нем чтото есть )то переходи на слудуюющюю страницу
            yield response.follow(next_page, callback=self.parse)                               #yeild делает это один раз
        for link in links:                                                                      #   yield - нужен для поочередного обхода каждой сылки
            yield response.follow(link, callback=self.parse_vacancy)                            #callback -  это асинхронная функция,к которой обращается response после получения сылки
    #
    #
    def parse_vacancy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").get()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)

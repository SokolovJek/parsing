'''Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.'''

from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
response = requests.get('https://lenta.ru/', headers=header)
dom = html.fromstring(response.text)

items = dom.xpath('//div[@class = "b-yellow-box__wrap"]/div[@class = "item"]')

a = 'https://lenta.ru'
news = []
for item in items:
    item_date = {}
    news_sourse = 'https://lenta.ru/'
    news1 = item.xpath('.//a/text()')
    news1 = " ".join(news1[0].split())  #удаляю лишние символы
    link1 = item.xpath('.//a/@href')
    link = a + link1[0]                    #делаю полноценную сылку
    date = '/'.join(link1[0].split('/')[2:5])

    item_date['источник'] = news_sourse
    item_date['новость'] = news1
    item_date['сылка'] = link
    item_date['дата'] = date
    news.append(item_date)
pprint(news)


client = MongoClient('localhost', 27017)
db = client['lesson4']
my = db.my
# my.insert_many(news)    --для добавления в БД
for i in my.find():
    print(i)



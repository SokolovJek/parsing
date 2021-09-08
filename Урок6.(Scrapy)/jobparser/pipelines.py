# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


'''pipline нужен для окончательного сбора информации и вывода ее! Здесь необхадимо сделать окончательную обработку данных 
,так как это финал и на ыходе у нас будет готовый словарь а тчнее объект похожий на словарь'''

class JobparserPipeline:

    def __init__(self):                                 # его создали мы (__init__ изначально не было)
        client = MongoClient('localhost', 27017)        # содаем подключение
        self.mongo_base = client.vacancy0609            # создаем БД


    def process_item(self, item, spider):
        item['min_salary'],item['max_salary'],item['curs']= self.salary(item['salary'], item['url'])  #обраьотка зарплаты(вариант)
        # dict_item = dicy(item)                                                                      #преобразуем к словарю и потом начинаем обработку   -эще один вариант обработки
        if 'superjob' in item['url']:          #если superjob:      (ПЕРЕГРУЗИЛ! лутше вызвал бы spider.name == 'superjob')
            if len(item['salary']) == 1:
                item['salary'] = item['salary'][0]
            else:
                a = ''.join(item['salary']).split()
                d = ' '.join(a)
                item['salary'] = d
        else:
            item['salary'] = ' '.join(item['salary'].split())
        """!!!! ЗДЕСЬ НУЖНО СОХРАНЯТЬ В БД, точка сохранения"""
        colection = self.mongo_base[spider.name]                                                     # создаем коленкцию в бд
        colection.insert_one(item)                                                                   # сохраняем коленкцию в бд
        return item

    def salary(self, salary, url):

        if 'superjob' not in url:                           #если hh.ru
            salary_split = salary.split()
            if len(salary_split) == 7:
                min = int(salary_split[1]+salary_split[2])
                max = int(salary_split[4]+salary_split[5])
                cur = salary_split[-1]
            elif len(salary_split) == 4 and salary_split[0] == 'от':
                min = int(salary_split[1] + salary_split[2])
                max = None
                cur = salary_split[-1]
            elif len(salary_split) == 4 and salary_split[0] == 'до':
                min = None
                max = int(salary_split[1] + salary_split[2])
                cur = salary_split[-1]
            else:
                min = None
                max = None
                cur = None
        elif 'superjob' in url:                                 #если superjob
            salary_split = ''.join(salary).split()
            if len(salary_split) == 4 and salary_split[0] != 'до' and salary_split[0] != 'от':
                min = int(salary_split[0]+salary_split[1][0:3])
                max = int(salary_split[1][3:] + salary_split[2])
                cur = salary_split[-1]
            elif len(salary_split) == 4 and salary_split[0] == 'до':
                min = None
                max = (salary_split[1] + salary_split[2])
                cur = salary_split[-1]
            elif len(salary_split) == 4 and salary_split[0] == 'от':
                min = int(salary_split[1] + salary_split[2])
                max = None
                cur = salary_split[-1]
            else:
                min = None
                max = None
                cur = None


        return min, max, cur
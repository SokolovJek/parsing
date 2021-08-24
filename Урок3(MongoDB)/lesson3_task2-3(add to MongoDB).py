"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""


from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36'}
url = 'https://volgograd.hh.ru/search/vacancy'

dict_job = []


client = MongoClient('localhost', 27017)
db = client['lesson3']
jobs = db.jobs



request_salary_min = int(input('укажите минимум по зарплате(Пр: 50000):'))


for i in range(1):

    params = {'clusters' : 'true', 'area' : 1, 'ored_clusters' : 'true', 'enable_snippets' : 'true', 'salary' : '', 'st':'searchVacancy', 'text' : 'Python'}
    params['page'] = int(i)
    response = requests.get(url, params=params,  headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_job = soup.find_all('div', {'class' : 'vacancy-serp-item'})


    for job in all_job:
        job_info = {}
        name = job.find('a', {'class': 'bloko-link'}).text
        link = job.find('a', {'class': 'bloko-link'})['href']
        city = job.find('span', {'data-qa' : 'vacancy-serp__vacancy-address'}).text
        site = url[:23]
        try:
            salary = job.find('span', {'data-qa' : "vacancy-serp__vacancy-compensation"}).text
            valute = salary.split()[-1]
            if len(salary.split()) == 6:
                min_salary = salary.split()[0] + salary.split()[1]
                max_salary = salary.split()[3] + salary.split()[4]

            elif len(salary.split()) == 4 and salary.split()[0] == 'от':
                min_salary = salary.split()[1] + salary.split()[2]
                max_salary = None

            else:
                min_salary = None
                max_salary = salary.split()[1] + salary.split()[2]
        except:
            min_salary = None
            max_salary = None
            valute = None



        job_info['site'] = site
        job_info['name'] = name
        job_info['link'] = link
        job_info['city'] = city
        try:
            job_info['min_salary'] = int(min_salary)
            job_info['max_salary'] = int(max_salary)
            job_info['valute'] = valute
        except:
            job_info['min_salary'] = min_salary
            job_info['max_salary'] = max_salary
            job_info['valute'] = valute

        try:
            if job_info['min_salary'] >= request_salary_min or job_info['max_salary'] >= request_salary_min:
                 pprint(job_info)
                 print('\n')
        except:
            pass

        jobs.update_one({'link': job_info['link']}, {'$set': job_info}, upsert=True)


f = 0
for i in jobs.find({}):
    f += 1
    pprint(i)
    print(f)





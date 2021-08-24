"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1.Наименование вакансии.
2.Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3.Ссылку на саму вакансию.
4.Сайт, откуда собрана вакансия.
5.По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в
json либо csv."""
from bs4 import BeautifulSoup
import requests, json
#https://volgograd.hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=Python

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36'}
url = 'https://volgograd.hh.ru/search/vacancy'

dict_job = []

for i in range(5):

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
            if len(salary.split()) == 6:
                min_salary = salary.split()[0] + salary.split()[1]
                max_salary = salary.split()[3] + salary.split()[4]
                valute = salary.split()[5]

            elif len(salary.split()) == 4 and salary.split()[0] == 'от':
                min_salary = salary.split()[1] + salary.split()[2]
                max_salary = None
                valute = salary.split()[3]


            else:
                min_salary = None
                max_salary = salary.split()[1] + salary.split()[2]
                valute = salary.split()[3]
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


        dict_job.append(job_info)

with open('job.json', 'w', encoding='utf-8') as f:
    json.dump(dict_job, f, ensure_ascii=False)

print(dict_job)
print(len(dict_job))


import csv

with open("job.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(["сайт", "должность", "сылка", 'город','мин. зарплата', 'макc. зарплата', 'валюта'])
    for job in dict_job:
        file_writer.writerow([job['site'], job['name'], job['link'],job['city'],job['min_salary'],job['max_salary'],job['valute']])

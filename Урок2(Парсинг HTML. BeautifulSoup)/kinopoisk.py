# https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://www.kinopoisk.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
params = {'quick_filters':'serials', 'tab':'all'}

response = requests.get(url+'/popular/films/', params=params, headers=headers)

soup = bs(response.text, 'html.parser')

serials = soup.find_all('div', {'class':'desktop-rating-selection-film-item'})

serials_list = []
for serial in serials:
    serial_data = {}

    info = serial.find('p',{'class':'selection-film-item-meta__name'})
#     name = info.text
#     link = url + info.parent.get('href')
#
#     genre = serial.find('span',{'class':'selection-film-item-meta__meta-additional-item'}).nextSibling.text
#     try:
#         rating = float(serial.find('span',{'class':'rating__value'}).text)
#     except:
#         rating = None
#
#     serial_data['name'] = name
#     serial_data['link'] = link
#     serial_data['genre'] = genre
#     serial_data['rating'] = rating
#
#     serials_list.append(serial_data)
#
# pprint(serials_list)
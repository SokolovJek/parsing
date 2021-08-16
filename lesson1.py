from pprint import pprint
import requests

city = 'Sochi'
my_params = {'q': city,
             'appid': 'e5e4cd692a72b0b66ea0a6b80255d1c3'}

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=my_params, headers=my_headers)

# response.headers.get('Content-Type')
# if response.status_code == 200:
#     print()
# response.text
# response.content

if response.ok:
    # pprint(response.text)
    j_data = response.json()

    print(f"Р’ РіРѕСЂРѕРґРµ {j_data.get('name')} С‚РµРјРїРµСЂР°С‚СѓСЂР° {round(j_data.get('main').get('temp') - 273.15, 2)} РіСЂР°РґСѓСЃРѕРІ")
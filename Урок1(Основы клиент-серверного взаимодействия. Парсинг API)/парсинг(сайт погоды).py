import requests

city = 'London'
app_key = 'f6bec3dad120a764f0f2435316f6be46'
response = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'q' : city, 'appid' : app_key, 'units' : 'metric'})
my_json = response.json()
print(f"Температура в {city} {my_json.get('main').get('temp')} градусов")
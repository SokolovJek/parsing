from lxml import html
from pprint import pprint
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get('https://ru.ebay.com/b/Fishing-Equipment-Supplies/1492/bn_1851047', headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//li[contains(@class,'s-item')]")

items_list = []
for item in items:
    items_data = {}
    name = item.xpath(".//h3[@class='s-item__title']/text()")
    link = item.xpath(".//h3[@class='s-item__title']/../@href")
    price = item.xpath(".//span[@class='s-item__price']//text()")
    info = item.xpath(".//span[contains(@class,'s-item__hotness')]//text()")

    items_data['name'] = name
    items_data['link'] = link
    items_data['price'] = price
    items_data['info'] = info

    items_list.append(items_data)

pprint(items_list)
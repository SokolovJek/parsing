
'''задача скачать файл(картинку): так можно делать но....
-нужно заранее знать формат файла
-нужно менять имя файла в ручном режиме()
-весь скачаный файл помещается в оперативную память(ОСЕНОВНОЙ МИНУС)'''
# import requests
#
# url = 'https://get.wallhere.com/photo/mountains-sky-nature-trees-1012973.jpg'
# response = requests.get(url)
# with open('image.jpg', 'wb') as f:
#     f.write(response.content)

'''задача скачать файл(картинку): лутше делать так'''
import wget
url = 'https://img1.fonwall.ru/o/ia/otkrytka-moya-milaya-osen-nature.jpeg?route=mid&h=750'
wget.download(url)


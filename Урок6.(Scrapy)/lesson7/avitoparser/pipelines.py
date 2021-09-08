# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline    #в scrapy имеется три класа для реализации скрапинга для картнок выбираем этот
import scrapy


class AvitoparserPipeline:      # создается в момент создания нашего проэкта      здесь необхадимо передавать все в БД
    def process_item(self, item, spider):  # В этот item попадаем после, потому что более низкий приоритет в settings
        print()
        return item


class AvitoPhotosPipeline(ImagesPipeline):  # В этот item попадаем сначала, потому что более высокий приоритет в settings    ЭТОТ КЛАСС ЗОЗДАЕМ МЫ!  НО НУЖНО СООБЩИТЬ ПАУКУ О ОЭТОМ КЛАССе по этому передаем в setings указания!
    def get_media_requests(self, item, info):    # также нужно передать в setings путь сохранения наших фотографий, а также нужно установить pillow(pip3 install pillow)
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(      #тут создается новая сесия(грубо говоря новый pesponse)
                        img)  # Скачиваем здесь фото и результат можно увидеть в след. методе item completed
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):        #этот метод создаем мы для связки скеваемых изображений(в папке photos) с обьявлением в БД
        item['photos'] = [itm[1] for itm in results if            # results это прикольная штука (по сути какраз в нем хранится связь папки photo и данных в БД(url)). МЫ передаем словарь с данными(url, где хранится,статус,название) заместо просто сылок(url) на фото
                          itm[0]]                                 # Здесь проверяем результат скачивания и сохраняем внутри item
        return item                                                 # и отправляем item для дальнейшей обработки(так как есть pipline с болие низким приоритетом)

    # def file_path(self, request, response=None, info=None, *, item=None):      # Метод для изменения места скачивания файлов
    #     pass




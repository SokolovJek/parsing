import scrapy
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem
from copy import deepcopy   # он нам нужен чтоб не было накладок(накладывания(вызов функции другим respons хотя еще с первого инфу не вытянули)) при создании query_hash в функции user_parse
from urllib.parse import urlencode    # позволит нам закинуть в variables наши данные(id, first)
import re    #импорт регулярныхъ выражений
import json

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login = '89247695715'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1631469844:Ae5QAN5x9sKHfXMdnDYSMW/jRBnHfgSQvRqsMdJ/Q3oJHMNsDZZiOemAwLEcyIJm1iVrCIW13tZMkP5aUQokRmKDxYlPf9bB9n7oEqLrdIB+VBvRGkvceT/o7s+qYAXJzdzhrCW6SnWKAIqhp+lRNE0='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'doctor_komarovskiy'   # это сылка для перехода на какойто акаунт(чтоб посмотреть, и парсить его)
    # posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    graphql_url = 'https://www.instagram.com/graphql/query/?'    # описание ниже (коротко это БД публикаций)
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'   # это хэш генерируемый единожды при прокручивании страницы(запрос на сервер для пролучения контента)



    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,    #FormRequest - этот класс позволяет делать запрос и отправлять данные
                                 method='POST',           #   POST делаем его потомучто у нас он используется при  запросе
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,    # этот параметр  используется в FormRequest
                                           'enc_password': self.insta_pwd},  # а в словарь копируем поля форм указанных при авторизации
                                 headers={'X-CSRFToken': csrf})     #потстовляем токен
    #
    #"""response.url----'https://www.instagram.com/accounts/login/ajax/'"""
    def user_login(self, response: HtmlResponse):  #после всещо что выше указанно, приходит сюда(проверить можно по 'response.text' где ответ '{"user":true,"userId":"13825842083","authenticated":true,"oneTapPrompt":true,"status":"ok"}')
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.parse_user}',
                                  callback=self.user_parse,   #мы по сути говорим перейди по сылке    (метод который получает ответ на гет запрос по этой сылке)
                                  cb_kwargs={'username': self.parse_user})   # так это тот параметр который помогает нам передавать информацию из ранее поолученых данных



    def user_parse(self, response: HtmlResponse, username): #следуюющий шаг попадаем сюда(переходим на страницу комаровский) здесь можем получить ниже указанное

        #нвчинаем разберать полученную страницу видим что публикаций 12,скролим и видим что появляются новые публикации и все это сопровождается вызовом через GET страници- '/graphql/query/?query_hash'
        # query_hash - здесь хранятся вооообще все публикации instagram
        # variables	{"id":"2101342990","first":12,"after":"....."
        # id - это данные(все публикации) пользователя -не уникальна
        # first - сколько получить(запрос)   - не уникальна
        # "after" - это автогенерируюющяяся строка отсносящаяяся к данному контенту(12 публикаций) - уникальна
        # при запросе через консоль response.url- 'https://www.instagram.com/doctor_komarovskiy/';   username -'doctor_komarovskiy'

        user_id = self.fetch_user_id(response.text, username)
        variables = {                       # "after"   - не указываем по скольку instagram сам его згенерирует и нам отдаст, причем 12 преывых а потом последующих
            'id': user_id,
            'first': 12
        }
        # при разборе кода ответа видим количество публикаций и "флаг": has_next_page - true а также ....
        # .... end_cursoк - QVFBbWhFVF9ZRGZiOHdlWWpOamxVeHV0OWhHdlRWTTFyZ0ROSDZ2VG5YdXhTbnJ3ejRhYk1HMVhrcjd6bktxQms0bHN3ZWJPQzZFZTlSLXo5SW5rZ1BoYQ==  который являится сылкой на след публикацию (наш after)
        # .... edges	[…] где хранятся данные про публикации и сылки на них!!!!!!
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'    # cобираем нащ query_hash

        yield response.follow(url_posts,  # делаем запрос посылке
                              callback=self.user_posts_parse,  # парсим данные
                              cb_kwargs={'username': username,  # тащим за собой дальше данные
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)}    # для каждого  будет свой variables (не будут перетиратся данные(не будет гонки))
                              )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):  # здесь мы парсим страницу и создаем новые запросы на следуюющие страницы (response.json() - есть все данные нужные для переходана на след порцию публикаций, а также данные про нынешнюю порцию
        print()
        if response.status == 200:
            j_data = response.json()   # выводит нам словарь (в котором все есть)
            page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info') # вытаскиваем данные о след спартии публикаций
            if page_info.get('has_next_page'):
                variables['after'] = page_info.get('end_cursor')
                url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
                yield response.follow(url_posts,
                                      callback=self.user_posts_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'variables': deepcopy(variables)})    # здесь у нас происходит пагинация(от слова page)- переход к след публикациям

            posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
            for post in posts:
                item = InstagramItem(user_id=user_id,       # формируем item
                                       username=username,
                                       photos=post.get('node').get('display_url'),                           # сылки на фото
                                       likes=post.get('node').get('edge_media_preview_like').get('count'),   # лайки
                                       post_data=post.get('node')   # а это полностью вся  node-а, чтоб если что то вытянуть дополниельные данные
                                       )
                yield item

    ##Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):    # берем инфу из  response.text, и выдергиваем через ругулярку id пользователя,  а username пердаем что ищем
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

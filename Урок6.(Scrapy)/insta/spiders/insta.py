import scrapy
from scrapy.http import HtmlResponse
from insta.items import InstaItem
import re
import json


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login = '#'  #      вводим логин
    insta_pwd = '#'    # вводим пароль
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user2 = 'amina128860'  # вводим пользователя кого парсим
    parse_user = 'sokolov_udachnyyi'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    url_1 = ''
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'



    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.parse_user}',
                                  callback=self.user_parse,
                                  cb_kwargs={'username': self.parse_user})
            yield response.follow(f'/{self.parse_user2}',
                              callback=self.user_parse,
                              cb_kwargs={'username': self.parse_user2})
#

    def user_parse(self, response: HtmlResponse, username):

        user_id = self.fetch_user_id(response.text, username)
        url_subscribers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page'
        url_subscriptions = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12'
        yield response.follow(url_subscribers,
                              headers={'User-Agent':'Instagram 155.0.0.37.107'},
                              callback=self.subscribers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'url_subscribers': url_subscribers})

        yield response.follow(url_subscriptions,
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                              callback=self.subscriptions_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'url_subscriptions': url_subscriptions})

 ###  тянем подписчиков
    def subscribers_parse(self, response: HtmlResponse, username, user_id, url_subscribers):
        a = response.json()
        subscribers = []
        for i in a.get('users'):

            id = {'user_id': i.get('pk'), 'name': i.get('username'), 'photo': i.get('profile_pic_url'),
                  'full_name': i.get('full_name')}
            subscribers.append(id)
        item = InstaItem(user_id= user_id,
                        username = username,
                        subscribers = subscribers)
        yield item

        if a.get('next_max_id'):
            url_subscribers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={a.get("next_max_id")}&search_surface=follow_list_page'
            yield response.follow(url_subscribers,  # делаем запрос посылке
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  callback=self.subscribers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'url_subscribers': url_subscribers})

#  тянем на кого подписан
    def subscriptions_parse(self, response: HtmlResponse, username, user_id, url_subscriptions):
        a = response.json()
        subscriptions = []
        for i in a.get('users'):
            id = {'user_id':i.get('pk'),'name':i.get('username'), 'photo':i.get('profile_pic_url'), 'full_name':i.get('full_name')}
            subscriptions.append(id)
        item = InstaItem(user_id=user_id,
                        username=username,
                        subscriptions=subscriptions)
        yield item

        if a.get('next_max_id'):
            url_subscriptions = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&max_id={a.get("next_max_id")}'
            yield response.follow(url_subscriptions,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  callback=self.subscriptions_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'url_subscriptions': url_subscriptions})

    # ##Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')


'''   ХЕШИРОВАНИЕ
mystring = 'Enter String to hash:'

# Предположительно по умолчанию UTF-8
hash_object = hashlib.sha1(mystring.encode())
print(hash_object.hexdigest())

f = len(mystring)

hash_object = hashlib.sha1()
hex_dig = hash_object.hexdigest()
'''



from pymongo import MongoClient
from pprint import pprint
import hashlib

client = MongoClient('localhost', 27017)   #данные по умолчаниб  (это обьект подключения к базе данных) или укажи IP

db = client['user1991']  #создание БД и название БД это ключ обьекта БД(пользователя)...может быть по желанию

users = db.users      # создаем колекцию        ==   users = db[users]

my_colections = [{'asdas',12},{"asdasd",123123},{'asdfasd',4444}]




# users.insert_one({                                            #   вставка данных
#                 '_id': '5',
#                 "name": "надя",
#                 "year": '2000','хоби':'find'})


# for user in users.find({'name': 'jek', "year": 1991}):                             #    варианты поиска    == and
#     pprint(user)
#
# for user in users.find({'$or':[{'name': 'jek'},{"_id": '3'}]}):                        #    варианты поиска  c    OR
#     pprint(user)
#
# for user in users.find({'year':{'$in':['1991',1991]}}):                               # варианты поиска  c    IN
#     pprint(user)



# for user in users.find({'year':{'$gt':'1999'}}):                                   # варианты поиска  c    __ > _
#     pprint(user)
# for user in users.find({'year':{'$lt':'1999'}}):                                   # варианты поиска  c    <
#     pprint(user)


# users.update_one({'_id': '6124cfe6'}, {'$set' : {'name': 'jon'}})         #   UPDATE  ONE  | add column

# users.update_one({'_id': '1'}, {'$set' : new_data })                              # UPDATE from variable

# users.update_many({}, {'$set' : {'my': 'cooool'}})                          #   UPDATE  MANY   |     ADD COLUMN

# users.replace_one({'_id': '1'}, new_data)                                         REPLASE VALUE


# users.update_one({'_id': '1'}, {'$set' : new_data }, upsert=True)  #*** 3 in 1 ищет докуметн и меняет его, если ненаходит то вставляет значение

new_data ={'_id': '1', 'lastname': 'Вова','firstname':'Обоимов', 'birthday': '1967-12-19'}

# users.delete_one({'_id':'3'})                                                   #   DELETE
users.delite_many({'_id': '1'})

for user in users.find({}):
    pprint(user)

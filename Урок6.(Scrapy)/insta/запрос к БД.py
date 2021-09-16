from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongo_base = client.insta


colection = mongo_base['sokolov_udachnyyi']

# получаем подписчиков
for user in colection.find({'username': 'sokolov_udachnyyi'}):
    try:
        print(user['subscribers'])
    except:
        pass
# получаем на кого подписан
for user in colection.find({'username': 'sokolov_udachnyyi'}):
    try:
        print(user['subscriptions'])
    except:
        pass
# import pymongo
from pymongo import MongoClient
import os


def init_db():
    a = os.environ['CLIENT']
    client = MongoClient(a)
    db = client['db']#создаем базу и названием db
    return db,client

def get_data(data,collection_name):
    db, cl = init_db()
    collection = db[collection_name]
    res = collection.find_one(data)
    cl.close()
    return res

def get_all(data,collection_name):
    db, cl = init_db()
    collection = db[collection_name]
    res = list(collection.find(data))
    cl.close()
    return res

def write_data(data,collection_name):#получаем из views data(корзина) и collection_name(имя колекции)
    db, cl = init_db()
    collection = db[collection_name]#добавляем колекцию
    collection.insert_one(data)#добавляем колекцию
    cl.close()

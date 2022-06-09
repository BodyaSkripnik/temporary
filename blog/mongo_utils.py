import pymongo

def init_db():
    client = pymongo.MongoClient('mongodb://docker:mongopw@localhost:55006')
    db = client['db']
    return db,client

def get_data(data,collection_name):
    db, cl = init_db()
    collection = db[collection_name]
    res = collection.find_one(data)
    cl.close()
    return res

def write_data(data,collection_name):
    db, cl = init_db()
    collection = db[collection_name]
    collection.insert_one(data)
    cl.close()

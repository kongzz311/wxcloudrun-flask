import time


def get_database(db_name):
    from pymongo import MongoClient
    import pymongo
    import os
    user = os.environ['user']
    pwd = os.environ['pwd']
    ip = os.environ['ip']

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb://{user}:{pwd}@{ip}:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name]


def addUser(qu, jie, id, ip):
    db = get_database('sam')
    collection = db['users']
    data = collection.find_one({'id': id})
    if data is None:
        data = {}
        data['id'] = id
    data['qu'] = qu
    data['jie'] = jie
    data['ip'] = ip
    data['time'] = time.time()
    x = collection.find_one_and_update(
        {'id': id},
        {'$set': data,
            #  "$currentDate": {"lastModified": True}
            },
        upsert=True
    )

def getUser(id):
    db = get_database('sam')
    collection = db['users']
    data = collection.find_one({'id': id})
    return data

def delUser(id):
    db = get_database('sam')
    collection = db['users']
    data = collection.delete_one({'id':id})
    return data
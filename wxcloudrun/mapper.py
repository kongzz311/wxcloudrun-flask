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


def getBlackList(ip):
    db = get_database('sam')
    collection = db['blackList']
    data = collection.find_one({'ip': ip})
    return data

def addUser(qu, jie, id, ip):
    if getBlackList(ip) is not None:
        print(f"ip blackList: {ip}")
        return
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
    data['del'] = False
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


def delUser(id, ip):
    db = get_database('sam')
    collection = db['users']
    data = collection.find_one({'id': id})
    if data is None:
        return data
    data['del'] = True
    data['time'] = time.time()
    data['ip'] = ip
    x = collection.find_one_and_update(
        {'id': id},
        {'$set': data,
         },
        upsert=True
    )
    return x


if __name__ == '__main__':
    print(getBlackList("192.168.3.201"))

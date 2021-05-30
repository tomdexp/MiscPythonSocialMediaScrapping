import json
from pymongo import MongoClient

def InsertJsonIntoMongodb():
    client = MongoClient("mongodb+srv://user_name:user_pass@cluster01.cpq4t.mongodb.net/test")
    db = client['social_media']
    collection = db['Post_collection']
    with open('table_post_records.json') as f:
        file_data = json.load(f)
    collection.insert_many(file_data)
    client.close()
    return

def ResetCollectionMongodb():
    client = MongoClient("mongodb+srv://user_name:user_pass@cluster01.cpq4t.mongodb.net/test")
    db = client['social_media']
    col = db["Post_collection"]
    x = col.delete_many({})
    print(x.deleted_count, " documents deleted.")
    client.close()
    return

# EXAMPLE : ResetCollectionMongodb()
# EXAMPLE : InsertJsonIntoMongodb()

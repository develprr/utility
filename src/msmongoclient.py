# Studied & written by Heikki Kupiainen 2023    

# Wrapper for a MongoDB client

import pymongo

class MSMongoClient(object):

  instance = None
  
  @classmethod
  @property
  def singleton(cls):
    if cls.instance is None:
        cls.instance = cls("msdb")
    return cls.instance
        
  def __init__(self, dbname):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    self.dbname = dbname
    self.client = myclient[dbname]
  
  def insert_one(self,collection_name, item):
    self.client[collection_name].insert_one(item)
  
  def find_one(self, collection_name, query):
    return self.client[collection_name].find_one(query)
  
  def aggregate(self, collection_name, pipeline):
    return self.client[collection_name].aggregate(pipeline)
  
  def find(self, collection_name, query):
    return list(self.client[collection_name].find(query))
  
  def delete_many(self, collection_name, query):
    return self.client[collection_name].delete_many(query)
      
def test_insert_one():
  client = MSMongoClient.singleton 
  client.insert_one("users", { "name": "Moctezuma" })
  entry = client.find_one("users")
  assert(entry["name"] == "Moctezuma")
# Studied & written by Heikki Kupiainen 2023    

# Wrapper for a MongoDB client

import pymongo
import os

from dotenv import load_dotenv

load_dotenv()

mongodb_address = os.getenv('MONGODB_ADDRESS')
mongodb_name = os.getenv('MONGODB_NAME')

class MSMongoClient(object):

  instance = None
  
  @classmethod
  @property
  def singleton(cls):
    if cls.instance is None:
        cls.instance = cls(mongodb_name)
    return cls.instance
        
  def __init__(self, dbname):
    myclient = pymongo.MongoClient(mongodb_address)
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
  
  def exists_collection(self, collection_name):
    return collection_name in self.collection_names()
  
  @cache
  def collection_names(self):
    return self.client.list_collection_names()
      
def test_insert_one():
  client = MSMongoClient.singleton 
  client.insert_one("users", { "name": "Moctezuma" })
  entry = client.find_one("users", {})
  assert(entry["name"] == "Moctezuma")

def test_exists_collection():
  assert(MSMongoClient.singleton.exists_collection("SoccerEvent") == True)
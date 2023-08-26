# (C) Heikki Kupiainen 2023    

# Wrapper for a MongoDB client

import pymongo

class MSMongoClient(object):

  def __init__(self, dbname):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    self.dbname = dbname
    self.client = myclient[dbname]
  
  def insert_one(self,collection_name, item):
    self.client[collection_name].insert_one(item)
  
  def find_one(self, collection_name):
    return self.client[collection_name].find_one()
      
def test_insert_one():
  database = MSDatabase("msdb") 
  database.insert_one("users", { "name": "Moctezuma" })
  entry = database.find_one("users")
  assert(entry["name"] == "Moctezuma")
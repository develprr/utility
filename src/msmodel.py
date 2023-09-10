# (C) Heikki Kupiainen 2023    

# MSModel is a study about combining Pydantic and MongoDB.
# By extending MSModel, a data object can be enabled to use
# Pydantic and persisted into Mongo database.

import orjson
import importlib
import sys,imp

from pydantic import BaseModel
from msmongoclient import MSMongoClient
  
class MSModel(BaseModel):

  # Converts data object to JSON with "_id" field which is compatible with MongoDB
  def to_json(self):
    json = orjson.loads(self.model_dump_json())
    id = json["id"]
    del json["id"]
    json["_id"] = id
    return json
    
  # insert object into DB
  def insert(self):
    collection_name = self.__class__.__name__
    return MSMongoClient.singleton.insert_one(collection_name, self.to_json())
  
  @classmethod
  def new_from_document(cls, document):  
    document["id"] = document["_id"]
    classname = cls.__name__
    modulename = classname.lower()
    module = importlib.import_module(modulename)
    class_ref = getattr(module, classname)
    return class_ref(**document)
    
  @classmethod
  def find_all(cls):
    collection_name = cls.__name__
    return MSMongoClient.singleton.find(collection_name, {})

  @classmethod
  def find_one(cls, query):
    collection_name = cls.__name__
    document =  MSMongoClient.singleton.find_one(collection_name, query)  
    return cls.new_from_document(document)
  
  @classmethod
  def delete_all(cls):
    collection_name = cls.__name__
    return MSMongoClient.singleton.delete_many(collection_name, {})
# (C) Heikki Kupiainen 2023    

# MSModel is a study about combining Pydantic and MongoDB.
# By extending MSModel, a data object can be enabled to use
# Pydantic and persisted into Mongo database.

import orjson
import importlib
from pydantic import BaseModel
from msmongoclient import MSMongoClient
  
class MSModel(BaseModel):

  # Converts data object to JSON with "_id" field which is compatible with MongoDB
  def to_mongo_json(self):
    json = orjson.loads(self.model_dump_json())
    return self.substitute_id_with_underscore_id(json)
  
  # when storing object to mongodb, expclit ID field must be translated into "_id"
  def substitute_id_with_underscore_id(self, json):
    id = json["id"]
    del json["id"]
    json["_id"] = id
    return json
    
  # insert object into DB
  def insert(self):
    collection_name = self.__class__.__name__
    return MSMongoClient.singleton.insert_one(collection_name, self.to_mongo_json())
  
  @classmethod
  def new_from_document(cls, document):  
    classname = cls.__name__
    modulename = classname.lower()
    module = importlib.import_module(modulename)
    class_ref = getattr(module, classname)
    document_with_id = {**document, "id": document["_id"]}
    return class_ref(**document_with_id)
    
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
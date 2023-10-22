# Studied and written by Heikki Kupiainen 2023    

# MSModel is a study about combining Pydantic and MongoDB.
# By extending MSModel, a data object can be enabled to use
# Pydantic and persisted into Mongo database.

import orjson
import importlib
from pydantic import BaseModel, StrictStr
from msmongoclient import MSMongoClient
  
class MSModel(BaseModel):

  id: StrictStr
  
  # Converts data object to JSON with "_id" field which is compatible with MongoDB
  def to_mongo_dict(self):
    dict = self.to_dict()
    return self.substitute_id_with_underscore_id(dict)
  
  def to_dict(self):
    return orjson.loads(self.model_dump_json())
  
  @classmethod
  def get_field_names(cls):
    return list(cls.model_fields.keys())
  
  def get_attribute_collection_name(self, attribute_name):
    return type(vars(self)[attribute_name]).__name__
    
  # when storing object to mongodb, expclit ID field must be translated into "_id"
  def substitute_id_with_underscore_id(self, json):
    id = json["id"]
    del json["id"]
    return {**json, '_id': id}
    
  # insert object into DB
  def insert(self):
    collection_name = self.__class__.__name__
    mongo_dict = self.to_mongo_dict()
    return MSMongoClient.singleton.insert_one(collection_name,  mongo_dict)
  
  @classmethod
  def new_from_document(cls, document):  
    
    # determine the target class into wich the Mongo document must be converted:
    classname = cls.__name__ 

    # determine the module in which the target class resides: 
    modulename = classname.lower()
    
    # import the actual module by the module name that we reasoned:
    module = importlib.import_module(modulename)
  
    # get a reference to the class object of the target class inside the module:
    class_ref = getattr(module, classname)

    # since our Pydantic objects are expected to have "id" field
    # whereas MongoDB document has an "_id" field
    # make a clone of the document that has "id" field:  
    document_with_id = {**document, "id": document["_id"]}
    
    # finally, create an instance of target class passing the document as constructor parameter:
    return class_ref(**document_with_id)
    
  @classmethod
  def find_all(cls):
    return cls.find({})

  @classmethod
  def find(cls, query):
    collection_name = cls.__name__
    documents = MSMongoClient.singleton.find(collection_name, query)
    return list(map(cls.new_from_document, documents))
    
  @classmethod
  def find_one(cls, query):
    collection_name = cls.__name__
    document = MSMongoClient.singleton.find_one(collection_name, query)  
    return cls.new_from_document(document)
  
  @classmethod
  def aggregate(cls, pipeline):
    collection_name = cls.__name__
    documents = MSMongoClient.singleton.aggregate(collection_name, pipeline)
    return list(map(cls.new_from_document, documents))
  
  @classmethod
  def aggregate_one(cls, pipeline):
    collection_name = cls.__name__
    documents = MSMongoClient.singleton.aggregate(collection_name, pipeline)
    return cls.new_from_document(list(documents)[0])
  
  @classmethod
  def delete_all(cls):
    collection_name = cls.__name__
    return MSMongoClient.singleton.delete_many(collection_name, {})
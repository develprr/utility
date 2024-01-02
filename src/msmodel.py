# Studied and written by Heikki Kupiainen 2023    

# MSModel is a study about combining Pydantic and MongoDB.
# By extending MSModel, a data object can be enabled to use
# Pydantic and persisted into Mongo database.

import orjson
import importlib
from pydantic import BaseModel, StrictStr
from msmongoclient import MSMongoClient
import numpy as np

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
    
  @classmethod
  def get_collection_references(cls):
    field_names = cls.get_field_names()
    return list(filter(cls.is_field_collection_reference, field_names))
  
  @classmethod
  def is_field_collection_reference(cls, field_name):
    field_type = cls.get_field_type(field_name)
    collection_names = MSMongoClient.singleton.collection_names()
    return True if field_type in collection_names else False
  
  @classmethod 
  def get_field_type(cls, field_name):
    return cls.model_fields[field_name].annotation;
    
  # Returns the name of the collection in the MongodB that is associated with given field name  
  @classmethod
  def get_field_type(cls, field_name):
    return cls.model_fields[field_name].annotation.__name__
  
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
    
  # Builds a one-to-one lookup object by field name.
  @classmethod
  def build_one_to_one_lookup(cls, field_name):
    collection_name = cls.get_field_type(field_name)
    local_field = f'{field_name}_id'
    return [
      {
        '$lookup': {
          'from': collection_name,
          'localField': local_field,
          'foreignField': '_id',
          'as': field_name
        }
      },
      {
        '$unwind': {
            'path': f'${field_name}',
            'preserveNullAndEmptyArrays': True
        }
      }
    ]
  
  @classmethod
  def build_one_to_one_lookups(cls):
    references = cls.get_collection_references()
    return np.array(list(map(cls.build_one_to_one_lookup, references))).flatten().tolist()
    
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
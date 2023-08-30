# (C) Heikki Kupiainen 2023    

# MSModel is Metamatic System's 
# ground-breaking base model to allow enabling
# two aspects to your business objects.
#
# Quickly convert your business data objects into Pydantic models
# and make them persistable into Mongo database
# by extending your models from MSModel base class!

import orjson
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
    MSMongoClient.singleton.insert_one(collection_name, self.to_json())
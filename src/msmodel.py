# (C) Heikki Kupiainen 2023    

# MSModel is a study about combining Pydantic and MongoDB.
# By extending MSModel, a data object can be enabled to use
# Pydantic and persisted into Mongo database.

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
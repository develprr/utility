# (C) Heikki Kupiainen 2023    

from pydantic import BaseModel, StrictStr, validate_call
import orjson
from msmongoclient import MSMongoClient
  
class Player(BaseModel):

  id: StrictStr
  name: StrictStr
  
  @staticmethod
  @validate_call
  def new(id: StrictStr, name: StrictStr):
    return Player(**{
      'id': id,
      'name': name
    })
    
  def to_json(self):
    json = orjson.loads(self.model_dump_json())
    id = json["id"]
    del json["id"]
    json["_id"] = id
    return json
    
  def insert(self):
    collection_name = self.__class__.__name__
    MSMongoClient.singleton.insert_one(collection_name, self.to_json())
  
def test_new():
  player = Player.new("21", "Ronaldinho Gaucho")
  assert(player.id == "21")
  assert(player.name == "Ronaldinho Gaucho")

def test_json():
  player = Player.new("21", "Ronaldinho Gaucho")
  json = player.to_json()
  print(json)
  player.insert()
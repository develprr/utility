# Studied & written by Heikki Kupiainen 

# Player is a Pydantic Mongo aware example class
# to demonstrate how to store and map your Pydantic models
# seamlessly to Mongo database.

from pydantic import StrictStr, validate_call
from msmodel import MSModel
  
class Player(MSModel):

  id: StrictStr
  name: StrictStr
  
  @staticmethod
  @validate_call
  def new(id: StrictStr, name: StrictStr):
    return Player(**{
      'id': id,
      'name': name
    })
    
  def get_description(self):
    return f"{self.name}: {self.id}"
      
def test_new():
  player = Player.new("21", "Ronaldinho Gaucho")
  assert(player.id == "21")
  assert(player.name == "Ronaldinho Gaucho")

def test_to_mongo_dict():
  player = Player.new("21", "Ronaldinho Gaucho")
  json = player.to_mongo_dict()
  assert(json == { "_id": "21", "name": "Ronaldinho Gaucho" })

def test_find_all():
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  Player.new("10", "Diego Maradona").insert()
  found_players = Player.find_all()
  assert(len(found_players) == 2)

def test_find_all__returns_a_list_of_player_objects():
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  Player.new("10", "Diego Maradona").insert()
  found_players = Player.find_all()
  for player in found_players:
    assert(type(player) == Player)
  
def test_delete_all(): 
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  Player.new("10", "Diego Maradona").insert()
  Player.delete_all()
  found_players = Player.find_all()
  assert(len(found_players) == 0)
  
def test_create_dynamically():
  player = eval("Player")(**{ "id": "21", "_id": "21", "name": "Ronaldinho Gaucho" })
  description = player.get_description()
  assert(description == "Ronaldinho Gaucho: 21")

def test_create_from_database():
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  player = Player.find_one({ "_id": "21" })
  description = player.get_description()
  assert(description == "Ronaldinho Gaucho: 21")
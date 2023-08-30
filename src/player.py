# (C) Heikki Kupiainen 2023    

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
      
def test_new():
  player = Player.new("21", "Ronaldinho Gaucho")
  assert(player.id == "21")
  assert(player.name == "Ronaldinho Gaucho")

def test_json():
  player = Player.new("21", "Ronaldinho Gaucho")
  json = player.to_json()
  assert(json == { "_id": "21", "name": "Ronaldinho Gaucho" })

def test_find_all():
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  Player.new("10", "Diego Maradona").insert()
  found_players = Player.find_all()
  assert(len(found_players) == 2)
  
def test_delete_all():
  Player.delete_all()
  Player.new("21", "Ronaldinho Gaucho").insert()
  Player.new("10", "Diego Maradona").insert()
  Player.delete_all()
  found_players = Player.find_all()
  assert(len(found_players) == 0)
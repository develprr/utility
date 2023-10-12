# A study about instantiating composite pydantic objects
# and serializing them in the Mongo database.

# Written by Heikki Kupiainen 2023    

from pydantic import StrictStr, validate_call
from msmodel import MSModel
from player import Player
from soccerevent import SoccerEvent

class EventAssignment(MSModel):

  event: SoccerEvent
  player: Player
  
  @staticmethod
  @validate_call
  def new(player: Player, event: SoccerEvent):
    return EventAssignment(**{
      'id': f'{player.id}:{event.id}',
      'player': player, 
      'event': event
    })
  
  # overwriting the default to_json() method
  # to store only references to property objects
  # instead of storing them as inline copies
  # inside the document:
  def to_dict(self):
    default_dict = super().to_dict()
    return {
      'id': self.id,
      'player_id': self.player.id,
      'event_id': self.event.id 
    }

  # fetch_one uses a custom MongoDB query to fetch
  # the event assignment object with its properties
  # in a format that can directly be deserialized
  # into a Pydantic EventAssignment composite object.
  @classmethod
  def fetch_one(cls, query):
    return cls.aggregate_one([
      {
        "$match": query
      },
      {
        "$lookup": {
          'from': 'Player',
          'localField': 'player_id',
          'foreignField': '_id',
          'as': 'player'
        }
      },
      {
        "$lookup": {
          'from': 'SoccerEvent',
          'localField': 'event_id',
          'foreignField': '_id',
          'as': 'event'
        }
      },
      {
        '$unwind': { 
            'path': '$player', 
            'preserveNullAndEmptyArrays': True 
        }
      },
      {
        '$unwind': { 
            'path': '$event', 
            'preserveNullAndEmptyArrays': True 
        }
      },
      {
        '$project': {
          'player.id': '$player._id',
          'player.name': 1,
          'event.id': '$event._id',
          'event.name': 1
        }
      }
    ]);
        
def test_new():
  player = Player.new("21", "R. Gaúcho")
  event = SoccerEvent.new("match")
  assignment = EventAssignment.new(player, event)
  assert(player.id == assignment.player.id)


# A complete Pydantic model structure can be
# directly instatiated from a nested dictionary object.
# This is fantastic!
def test_constuctor__works_with_nested_dictionary_object():
  player = Player.new("21", "R. Gaúcho")
  event = SoccerEvent.new("match")
  assignment = EventAssignment(**{
    'id': f'{player.id}:{event.id}',
    'player': {
        'id': '21',
        'name':  'R. Gaúcho'
     },
     'event': {
        'id': 'some-event-id',
        'name': 'match'
     }
  })
  
  assert(assignment.player.id == '21')
  assert(assignment.event.id == 'some-event-id')
  assert(assignment.event.name == 'match')

def test_fetch_one():
  EventAssignment.delete_all()
  SoccerEvent.delete_all()
  Player.delete_all()
  
  player = Player.new("21", "R. Gaúcho")
  event = SoccerEvent.new("match")

  player.insert()
  event.insert()

  assignment = EventAssignment.new(player, event)
  assignment.insert()
  
  found_assignment = EventAssignment.fetch_one({ '_id' : assignment.id});
  assert(found_assignment.id == assignment.id)
  assert(found_assignment.player.name == "R. Gaúcho")
  
def test_insert_one():
  player = Player.new("21", "R. Gaúcho")
  event = SoccerEvent.new("match")
  EventAssignment.delete_all()
  assignment = EventAssignment.new(player, event)
  assignment.insert()
  found_assignment = EventAssignment.find_one({})
  assert(found_assignment.id == assignment.id)
  assert(assignment.event.name == event.name)

def test_to_dict():
  player = Player.new("21", "R. Gaúcho")
  event = SoccerEvent.new("match")
  assignment = EventAssignment.new(player, event)
  dictionary = assignment.to_dict()
  expected_dictionary = { 
    'id': f'{player.id}:{event.id}', 
    'event_id': event.id, 
    'player_id': player.id
  }
  assert(dictionary == expected_dictionary)
# (C) Heikki Kupiainen @ Metamatic Systems 2023    

from pydantic import StrictStr, validate_call
from msmodel import MSModel
import uuid

class SoccerEvent(MSModel):

  id: StrictStr
  name: StrictStr
  
  @staticmethod
  @validate_call
  def new(name: StrictStr):
    return SoccerEvent(**{
      'id': str(uuid.uuid4()),
      'name': name
    })

def test_find_all():
  SoccerEvent.delete_all()
  SoccerEvent.new("Excercise").insert()
  SoccerEvent.new("Match").insert()
  found_events = SoccerEvent.find_all()
  assert(len(found_events) == 2)
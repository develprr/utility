# (C) Heikki Kupiainen @ Metamatic Systems 2023    

# MSEpoch represents time in milliseconds passed after the 
# great Epoch event, which was on 1st January 1970 at midnight in GMT time zone.

from pydantic import BaseModel, StrictStr, ConfigDict, validate_call
from datetime import datetime

class MSEpoch(BaseModel):
    
  time: int
  
  @staticmethod
  @validate_call
  def new_from_datetime(datetime: datetime):
    return MSEpoch(**{
      'time': datetime.timestamp() * 1000
    })   
   
  @staticmethod
  @validate_call
  def new_from_iso(iso: StrictStr):
    time = datetime.fromisoformat(iso)
    return MSEpoch.new_from_datetime(time)
    
def test_new_from_iso():
  time = MSEpoch.new_from_iso("1970-01-01T00:00:00+00:00").time
  assert(time == 0)
  time = MSEpoch.new_from_iso("1970-01-01T00:00:00+01:00").time  
  one_hour_in_ms = 60 * 60 * 1000
  assert(time == 0 - one_hour_in_ms)
# (C) Metamatic Systems 2023    

# A Pydantic based wrapper for string lists to ensure
# type safety of string list objects.

from typing import List
from pydantic import BaseModel, StrictStr

class StringList(BaseModel):
  list: List[StrictStr]
  
  @staticmethod
  def new(strings: List[StrictStr]):
    return StringList(**{
      'list': strings
    })

def test_instantiation():
  assert(type(StringList.new(['list', 'of', 'words']))) == StringList
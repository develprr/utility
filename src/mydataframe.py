# (C) Heikki Kupiainen 2023    

import pandas
from typing import List
from pydantic import BaseModel, StrictStr, ConfigDict, ValidationError, validate_call

class MyDataFrame(BaseModel):

  model_config = ConfigDict(arbitrary_types_allowed=True)
  
  @staticmethod
  @validate_call
  def create_from_dict(dictionary: dict):
      return pandas.DataFrame(dictionary)
      
  def __init__(self, data):
    self.data = data


def test_create_from_dict__fail_on_wrong_parameter_type():
  try:
    dataframe = MyDataFrame.create_from_dict([1,2,3])
  except:
    print("pass: exception was raised as expected")
    return
  raise Exception("fail: exception was not raised")
    
def test_create_from_dict__pass_when_created_from_dict():
  data = {
      'apples': [3, 2, 0, 1], 
      'oranges': [0, 3, 7, 2]
  }
  assert(type(data)) == dict
  dataframe = MyDataFrame.create(data)
  assert(type(dataframe)) == pandas.core.frame.DataFrame
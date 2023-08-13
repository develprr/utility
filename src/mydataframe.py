# (C) Heikki Kupiainen 2023    

import pandas
from typing import List
from pydantic import BaseModel, StrictStr, ConfigDict, ValidationError, validate_call

class MyDataFrame(BaseModel):

  model_config = ConfigDict(arbitrary_types_allowed=True)
  
  dataframe: pandas.core.frame.DataFrame
  
  
  @staticmethod
  @validate_call(config=dict(arbitrary_types_allowed=True))
  def new(dataframe: pandas.core.frame.DataFrame):
    return MyDataFrame(**{
      'dataframe': dataframe
    })
  @staticmethod
  @validate_call
  def create_from_dict(dictionary: dict):
    dataframe = pandas.DataFrame(dictionary)
    return MyDataFrame.new(dataframe)
  
  @validate_call
  def add_index(self, index: list[str]):
    indexed_dataframe = pandas.DataFrame(self.dataframe, index)
    self.dataframe = indexed_dataframe
    return self.dataframe
    
  def print(self):
    print(dataframe)
    
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
  dataframe = MyDataFrame.create_from_dict(data)
  assert(type(dataframe)) == MyDataFrame

def test_add_index__pass_on_string_list():
  data = {
      'apples': [3, 2, 0, 1], 
      'oranges': [0, 3, 7, 2]
  }
  dataframe = MyDataFrame.create_from_dict(data)
  dataframe = dataframe.add_index(["June", "Robert", "Lily", "David"])
  print(dataframe)
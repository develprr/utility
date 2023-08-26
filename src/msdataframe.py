# (C) Metamatic Systems 2023    

# MSDataFrame is a wrapper utility for Pandas dataframes.
# MSDataFrame provides type-safe constructors
# to instantiate a data frame from a 2-dimensional float array 
# and a from a simple list of float values.

import pandas
import json
from pydantic import BaseModel, ConfigDict, validate_call
from d2floatarray import D2FloatArray
from stringlist import StringList

class MSDataFrame(BaseModel):

  model_config = ConfigDict(arbitrary_types_allowed=True)
  
  dataframe: pandas.core.frame.DataFrame
  
  @staticmethod
  @validate_call
  def new_from_list(list: list[float]):
    return MSDataFrame(**{
      'dataframe': pandas.DataFrame(list)
    })

  @staticmethod
  @validate_call
  def new_from_d2_float_array(d2array: D2FloatArray, columns: StringList):
    return MSDataFrame(**{
      'dataframe': pandas.DataFrame(d2array.ndarray.T, columns.list)
    })
    
  def __str__(self):
    return str(self.dataframe)
    
  def to_json(self):
    return json.dumps(json.loads(self.dataframe.to_json(orient="columns")))

def test_new_from_list__pass_with_list():
  ms_dataframe = MSDataFrame.new_from_list([1,2,3])
  assert(type(ms_dataframe)) == MSDataFrame    

def test_new_from_d2_float_array__pass_with_ms_float_array():
  float_array = D2FloatArray.new([[161,47],[170.5, 72.4],[185.5, 91]])
  columns = StringList.new(['Weight', 'Height'])
  ms_dataframe = MSDataFrame.new_from_d2_float_array(float_array, columns)
  assert(type(ms_dataframe)) == MSDataFrame
  
def test_new_from_d2_float_array__fail_with_non_string_list_columns():
  float_array = D2FloatArray.new([[161,47],[170.5, 72.4],[185.5, 91]])
  try:
    columns = StringList.new(['Weight', 12])
    ms_dataframe = MSDataFrame.new_from_d2_float_array(float_array, columns)
  except:
    print("pass: an exception was raised as expected on instantiation of wrong kinds of objects")
    return
  raise Exception("fail: an exception was not raised on wrong constructor parameters")    

def test_to_json():
  float_array = D2FloatArray.new([[161,47],[170.5, 72.4],[185.5, 91]])
  columns = StringList.new(['Weight', 'Height'])
  ms_dataframe = MSDataFrame.new_from_d2_float_array(float_array, columns)
  json = ms_dataframe.to_json()
  expected_json = '{"0": {"Weight": 161.0, "Height": 47.0}, "1": {"Weight": 170.5, "Height": 72.4}, "2": {"Weight": 185.5, "Height": 91.0}}'
  assert(ms_dataframe.to_json() == expected_json)
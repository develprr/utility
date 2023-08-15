# (C) Metamatic Systems 2023    

# D2FloatArray is a type safe wrapper & initializer for a two dimensional ndarray containing float values

from pydantic import BaseModel, ConfigDict, validate_call

import numpy as np
from numpy import ndarray
  
class D2FloatArray(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
    
  ndarray: ndarray

  @staticmethod
  @validate_call
  def new(array: list[list[float]]):
    return D2FloatArray(**{
      'ndarray': np.array(array)
    })

# Perhaps surprisingly, this must pass because an int list is also a float list although a float list is not an int list.
def test_new__pass_when_three_int_lists_are_given():
  array = D2FloatArray.new([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).ndarray
  assert(array.dtype.name) == "float64"

def test_new__fail_when_arbitrary_lists_are_given():
  try:
    array = D2FloatArray.new([1, 2, 3], ["neljä", 5, 6]).ndarray
  except:
    print("pass: exception was raised as expected")
    return
  raise Exception("fail: exception was not raised as expected")
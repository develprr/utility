# (C) Heikki Kupiainen 2023    

# MSArray is a type safe wrapper & initializer for ndarray 

from typing import List
from pydantic import BaseModel, StrictStr, ConfigDict, ValidationError, validate_call

import numpy as np
from numpy import ndarray
  
class D2Array(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
    
  ndarray: ndarray

  @staticmethod
  @validate_call
  def new_from_lists(list1: list[float], list2: list[float]):
    return D2Array(**{
      'ndarray': np.array([list1, list2])
    })

  # Perhaps urprisingly, this must pass because an int list is also a float list although a float list is not an int list.
  # Just like every dog is an animal but not every animal is a dog :) 
  def test_new_from_lists__pass_when_two_int_lists_are_given():
    array = MSArray.new_from_lists([1, 2, 3], [4, 5, 6]).ndarray
    assert(array.dtype.name) == "float64"

def test_new_from_lists__fail_when_arbitrary_lists_are_given():
  try:
    array = D2Array.new_from_lists([1, 2, 3], ["neljä", 5, 6]).ndarray
  except:
    print("pass: exception was raised as expected")
    return
  raise Exception("fail: exception was not raised as expected")
# (C) Heikki Kupiainen 2023    
# MSTable object represents a data table with columns and rows.

import pandas
import json
from pydantic import BaseModel, ConfigDict, validate_call
from d2floatarray import D2FloatArray
from stringlist import StringList

class MSTable(BaseModel):

  model_config = ConfigDict(arbitrary_types_allowed=True)  
  
  dataframe: pandas.core.frame.DataFrame    
  
  @staticmethod
  @validate_call
  def new(columns: StringList, rows: D2FloatArray):
    data = {}
    d2list = rows.tolist()
    for column_index, column in enumerate(columns.list):
      if not column in data:
        data[column] = []
      for row_index, row in enumerate(d2list):
        data[column].append(row[column_index])
    return MSTable(**{
      'dataframe': pandas.DataFrame(data)
    })
  
  def to_json(self):
    return json.dumps(json.loads(self.dataframe.to_json(orient="columns")))
    
def test_to_json():
  table = MSTable.new(
    StringList.new(
      ["height", "weight"]
    ),
    D2FloatArray.new([
      [161, 52],
      [191, 89]
    ])
  )
   
  assert(table.to_json() == json.dumps({"height": {"0": 161.0, "1": 191.0}, "weight": {"0": 52.0, "1": 89.0}}))
import pandas as pd
from KOMPOTpy.kompotable import get_index_of_closest_number

data = pd.DataFrame({"data": [1,1,1,1,1,2,3,3,3,4,50,51,52,55,58,69,69,69,73,75,80,89,95,96,97,98,98,99,100]})

def test_datatype():
    idx = get_index_of_closest_number(data["data"],42)
    assert isinstance(idx,int)

def test_output():
    idx1 = get_index_of_closest_number(data["data"], 1.5)
    idx2 = get_index_of_closest_number(data["data"], 42)
    idx3 = get_index_of_closest_number(data["data"], 420)

    assert idx1 == 0
    assert idx2 == 10
    assert idx3 == len(data) - 1
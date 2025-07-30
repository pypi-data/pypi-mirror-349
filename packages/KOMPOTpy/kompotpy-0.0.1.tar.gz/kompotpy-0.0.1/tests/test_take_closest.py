import numpy as np
from KOMPOTpy.kompotable import take_closest

data1 = [1,1,1,1,1,2,3,3,3,4,50,51,52,55,58,69,69,69,73,75,80,89,95,96,97,98,98,99,100]
data2 = np.multiply(data1,0.33)


def test_datatype_int():
    closest = take_closest(data1,5)
    assert isinstance(closest,int)

def test_datatype_float():
    closest = take_closest(data2,5)
    assert isinstance(closest,float)

def test_output():
    closest1 = take_closest(data1, 71)
    closest2 = take_closest(data1, 200)
    closest3 = take_closest(data1, -16)

    assert closest1 == 69
    assert closest2 == 100
    assert closest3 == 1
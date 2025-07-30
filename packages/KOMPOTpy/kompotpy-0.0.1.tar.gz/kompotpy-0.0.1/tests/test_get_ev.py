import math


from KOMPOTpy.kompotable import get_ev

def test_datatype_tuple():
    ev = get_ev((69, 420), tuple = True)
    assert isinstance(ev,tuple)

def test_datatype_float():
    ev = get_ev(42, tuple = False)
    assert isinstance(ev,float)

def test_output_tuple():
    ev = get_ev((69, 420), tuple = True)
    true_upper = 17.968723188406
    true_lower = 2.9520045952380953
    assert math.isclose(ev[0],true_lower, rel_tol = 1e-6)
    assert math.isclose(ev[1],true_upper, rel_tol = 1e-6)

def test_output_float():
    ev = get_ev(69, tuple = False)
    true_ev = 17.968723188406
    assert math.isclose(ev,true_ev, rel_tol = 1e-6)


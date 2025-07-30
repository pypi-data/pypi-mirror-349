import math


from KOMPOTpy.kompotable import get_wavelength

def test_datatype_tuple():
    wavelength = get_wavelength((69, 420), tuple = True)
    assert isinstance(wavelength,tuple)

def test_datatype_float():
    wavelength = get_wavelength(42, tuple = False)
    assert isinstance(wavelength,float)

def test_output_tuple():
    wavelength = get_wavelength((69, 420), tuple = True)
    true_upper = 17.968723188406
    true_lower = 2.9520045952380953
    assert math.isclose(wavelength[0],true_lower, rel_tol = 1e-6)
    assert math.isclose(wavelength[1],true_upper, rel_tol = 1e-6)

def test_output_float():
    wavelength = get_wavelength(69, tuple = False)
    true_wavelength = 17.968723188406
    assert math.isclose(wavelength,true_wavelength, rel_tol = 1e-6)



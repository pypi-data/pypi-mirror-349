import pandas as pd
import pytest
from KOMPOTpy.kompotable import KOMPOT

# Sample mock fixed-width text data (fake structure for testing)
mock_table = """\
This is a useless line that will get cut
This one too
Did you ever hear the tragedy of Darth Plagueis the wise? I thought not. It's not a story the Jedi would tell you.
index   Altitude_(cm)   Human       Dwarf       Elf         Hobbit      Wizard      Servant_of_Sauron       0.5      0.6     0.7     0.8     0.9     1.0
0       0               Aragorn     Gimli       Legolas     Merry       Gandalf     Witchking_of_Angmar     1.0      2.0     3.0     4.0     5.0     6.0
1       10000           Theoden     Thorin      Arwen       Pippin      Radagast    Gothmog                 1.1      2.1     3.1     4.1     5.1     6.1
"""

@pytest.fixture
def sample_file(tmp_path):
    file = tmp_path / "test_data.txt"
    file.write_text(mock_table)
    return str(file)

def test_path(sample_file):
    kompot = KOMPOT(sample_file)
    assert kompot.path == sample_file

def test_file(sample_file):
    kompot = KOMPOT(sample_file)
    assert isinstance(kompot.file, pd.DataFrame)

def test_shape(sample_file):
    kompot = KOMPOT(sample_file)
    assert kompot.shape == (2,14)

def test_integrated_flux_datatype(sample_file):
    kompot = KOMPOT(sample_file)
    flux = kompot.get_integrated_flux(0,(1,5))
    assert isinstance(flux, float)

def test_integrated_flux_output(sample_file):
    kompot = KOMPOT(sample_file)
    flux = kompot.get_integrated_flux(0, (1, 6.5))
    assert flux == 21.0

def test_integrated_flux_out_of_bounds(sample_file):
    kompot = KOMPOT(sample_file)
    flux = kompot.get_integrated_flux(0, (42, 69))
    assert flux == 0.0



import pytest
from scorpy import CifData

from pathlib import Path


TEST_DIR = Path(__file__).parent

DATA_PATH = TEST_DIR / "data"



def test_load():
    c = CifData(path=DATA_PATH/ "1AL1-sf.cif")
    c = CifData(path=str(DATA_PATH/ "1AL1-sf.cif"))



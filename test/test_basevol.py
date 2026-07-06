

import pytest
from scorpy import BaseVol





def test_save(tmp_path):
    b1 = BaseVol(30, 40, 50, 1, 2, 3, 5, 6,7, False, False, False, False,)
    tmp_file_path = tmp_path / "b1.npy"
    b1.save(tmp_file_path)
    b1.save(str(tmp_file_path))














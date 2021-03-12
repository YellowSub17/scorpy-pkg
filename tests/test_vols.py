#!/usr/bin/env python3
import unittest
import scorpy
import numpy as np
from pathlib import Path
np.random.seed(0)


class TestVol(unittest.TestCase):

    def setUp(self):
        self.v_nx = 10
        self.v_ny = 20
        self.v_nz = 30
        self.v_xmax = 1
        self.v_ymax = 2
        self.v_zmax = 3

        self.v_path ='./data/test_vol'
        self.v_pathlib = Path('./data/test_vol') 

        self.v = scorpy.Vol(self.v_nx, self.v_ny, self.v_nz, \
                            self.v_xmax, self.v_ymax, self.v_zmax)

    def test_setvol(self):
        self.v.vol = np.ones(self.v.vol.shape)
        self.assertEqual(self.v.vol.sum(), self.v_nx*self.v_ny*self.v_nz)



    def test_savevol_str(self):
        self.v.save_dbin(self.v_path)

    def test_savevol_pathlib(self):
        self.v.save_dbin(self.v_pathlib)




    def test_saveloadvol(self):
        self.v.vol = np.random.random(self.v.vol.shape)
        self.v.save_dbin(self.v_path)
        v_loaded = scorpy.Vol(path=self.v_path)
        np.testing.assert_array_equal(v_loaded.vol, self.v.vol)














if __name__ == '__main__':
    unittest.main()


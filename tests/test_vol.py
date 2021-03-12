#!/usr/bin/env python3
import unittest
import pytest

import scorpy

import sys, os
from pathlib import Path
import numpy as np
np.random.seed(0)


data_for_test_path = Path(__file__).parent / 'data_for_tests'



class VolTests(unittest.TestCase):

    def setUp(self):
        self.v_nx = 10
        self.v_ny = 20
        self.v_nz = 30
        self.v_xmax = 1
        self.v_ymax = 2
        self.v_zmax = 3

        self.v_path =f'{data_for_test_path}/tmp/tmp_vol'

        self.v = scorpy.Vol(self.v_nx, self.v_ny, self.v_nz, \
                            self.v_xmax, self.v_ymax, self.v_zmax)


    def tearDown(self):
        tmp_dir = os.listdir(f'{data_for_test_path}/tmp/')
        for file in tmp_dir:
            os.remove(f'{data_for_test_path}/tmp/{file}')




    @pytest.mark.run(order=99)
    def test_setvol(self):
        '''
        Various test for manipulating v.vol
        '''
        # direct assigning
        self.v.vol = np.ones(self.v.vol.shape)
        self.assertEqual(self.v.vol.sum(), self.v_nx*self.v_ny*self.v_nz)

        # assignment operator
        self.v.vol += np.ones(self.v.vol.shape)
        self.assertEqual(self.v.vol.sum(), 2*self.v_nx*self.v_ny*self.v_nz)

        self.v.vol += 1
        self.assertEqual(self.v.vol.sum(), 3*self.v_nx*self.v_ny*self.v_nz)

        self.v.vol *= 2
        self.assertEqual(self.v.vol.sum(), 6*self.v_nx*self.v_ny*self.v_nz)

        # can't set vol to new shaped array
        with self.assertRaises(AssertionError):
            self.v.vol = np.ones( (self.v_nx-1, self.v_ny-1, self.v_nz-1))




    def test_saveloadvol_str(self):
        '''
        test for saving and loading vols from string
        '''
        self.v.vol = np.random.random(self.v.vol.shape)
        self.v.save_dbin(self.v_path)
        v_loaded = scorpy.Vol(path=self.v_path)
        np.testing.assert_array_equal(self.v.vol, v_loaded.vol)



    def test_saveloadvol_path(self):
        '''
        test for saving and loading vols from path
        '''
        self.v.vol = np.random.random(self.v.vol.shape)
        self.v.save_dbin(Path(self.v_path))
        v_loaded = scorpy.Vol(path=Path(self.v_path))
        np.testing.assert_array_equal(self.v.vol, v_loaded.vol)



















if __name__ == '__main__':
    unittest.main()



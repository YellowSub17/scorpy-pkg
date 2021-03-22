#!/usr/bin/env python3
import unittest
import pytest

import scorpy

import sys, os
from pathlib import Path
import numpy as np
np.random.seed(0)


data_for_test_path = Path(__file__).parent / 'data_for_tests' / 'cifdata'




class CifDataTests(unittest.TestCase):

    def setUp(self):
        self.cif_path = f'{data_for_test_path}/test-sf.cif'
        self.cif = scorpy.CifData(self.cif_path)
        self.qmax = 0.1



    def tearDown(self):
        pass


    def test_limitqmax(self):
        '''
        test for limiting qmax
        '''
        cif = scorpy.CifData(self.cif_path, qmax=self.qmax)
        self.assertEqual(cif.qmax, self.qmax)

    def test_symgroup(self):
        '''
        test if symgroup is correctly saved
        '''
        self.assertEqual(self.cif.space_group, 'I 41 3 2' )

    def test_dcellvecs(self):
        '''
        test if direct lattice cell vectors are calculated
        '''
        np.testing.assert_array_almost_equal(self.cif.dcell_vectors[0],\
                                             62.35*np.array([1, 0, 0]))
        np.testing.assert_array_almost_equal(self.cif.dcell_vectors[1],\
                                             62.35*np.array([0, 1, 0]))
        np.testing.assert_array_almost_equal(self.cif.dcell_vectors[2],\
                                             62.35*np.array([0,0,1]))
    def test_cellangles(self):
        '''
        test if direct lattice cell angles are calculated
        '''
        self.assertEqual(self.cif.dcell_angles[0], np.radians(90))
        self.assertEqual(self.cif.dcell_angles[1], np.radians(90))
        self.assertEqual(self.cif.dcell_angles[2], np.radians(90))

    def test_qcellvecs(self):
        '''
        test if reciprocal lattice vectors are calculated
        '''
        np.testing.assert_array_almost_equal(self.cif.qcell_vectors[0],\
                                            1/62.35*np.array([1, 0, 0]))
        np.testing.assert_array_almost_equal(self.cif.qcell_vectors[1],\
                                            1/62.35*np.array([0, -1, 0]))
        np.testing.assert_array_almost_equal(self.cif.qcell_vectors[2],\
                                            1/62.35*np.array([0,0,1]))

    def test_multiplicity(self):
        '''
        test if symetry is working
        '''
        self.assertEqual(self.cif.scattering.shape[0],2*48)

    def test_sphericalbound(self):
        '''
        test if spherical coords are with bounds
        '''
        self.assertLessEqual(np.max(self.cif.spherical[:,0]), self.cif.qmax)
        self.assertLessEqual(np.max(self.cif.spherical[:,1]), np.pi)
        self.assertLessEqual(np.max(self.cif.spherical[:,2]), np.pi*2)

        self.assertGreaterEqual(np.min(self.cif.spherical[:,0]),0)
        self.assertGreaterEqual(np.min(self.cif.spherical[:,1]),0)
        self.assertGreaterEqual(np.min(self.cif.spherical[:,2]),0)




if __name__ == '__main__':
    unittest.main()



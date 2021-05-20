#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestCifData(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_cell_angles(self):
        cif = scorpy.CifData(f'{test_data_dir}/cifdata/cell-angles.cif')
        self.assertEqual(np.radians(10), cif.alpha)
        self.assertEqual(np.radians(20), cif.beta)
        self.assertEqual(np.radians(30), cif.gamma)

    def test_cell_vectors(self):
        cif = scorpy.CifData(f'{test_data_dir}/cifdata/cell-vectors.cif')
        a = np.array([1,0,0])
        b = np.array([0,2,0])
        c = np.array([0,0,3])
        np.testing.assert_array_equal(a, cif.a)
        np.testing.assert_array_equal(b, cif.b)
        np.testing.assert_array_equal(c, cif.c)

    # def test_cell_properties(self):
        # cif = scorpy.CifData(f'{test_data_dir}/cifdata/cell-testing.cif')
        # a = np.array([1,0,0])
        # b = np.array([np.sqrt(2), np.sqrt(2),0])

        # c = np array(





        # c_unit = np.array([
            # np.cos(self.beta),
            # (np.cos(self.alpha) - np.cos(self.beta) *
             # np.cos(self.gamma)) / np.sin(self.gamma),
            # np.sqrt(1 - np.cos(self.beta)**2 - ((np.cos(self.alpha) -
                                                 # np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma))**2)
        # ])


        # np.testing.assert_array_equal(a, cif.a)
        # np.testing.assert_array_equal(b, cif.b)
        # np.testing.assert_array_equal(c, cif.c)




    # def test_properties(self):
        # '''
        # Test that every property in the object matches the input and is accessable
        # '''
        # for prop in self.properties:
            # stmt = f'''
# self.assertEqual(self.{prop}, self.vol.{prop}, msg="Failed at {prop}")
            # '''
            # exec(stmt)













if __name__ == '__main__':
    unittest.main()

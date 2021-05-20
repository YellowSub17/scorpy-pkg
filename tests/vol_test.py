#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestVol(unittest.TestCase):

    def setUp(self):

        self.nx = 6
        self.ny = 10
        self.nz = 12

        self.xmax = 6
        self.ymax = 1.4
        self.zmax = 180

        self.xmin = 0
        self.ymin = -2.2
        self.zmin = 0

        self.xwrap = False
        self.ywrap = False
        self.zwrap = True

        self.vol = scorpy.Vol(self.nx, self.ny, self.nz,
                              self.xmax, self.ymax, self.zmax,
                              self.xmin, self.ymin, self.zmin,
                              self.xwrap, self.ywrap, self.zwrap)

        self.properties = ['nx', 'ny', 'nz',
                           'xmax', 'ymax', 'zmax',
                           'xmin', 'ymin', 'zmin',
                           'xwrap', 'ywrap', 'zwrap']
        self.axes = ['x','y','z']

    def tearDown(self):
        pass



    def test_properties(self):
        '''
        Test that every property in the object matches the input and is accessable
        '''
        for prop in self.properties:
            stmt = f'''
self.assertEqual(self.{prop}, self.vol.{prop}, msg="Failed at {prop}")
            '''
            exec(stmt)


    def test_write_protection(self):
        '''
        Test that every property is write protected
        '''
        for prop in self.properties:
            stmt = f'''
with self.assertRaises(AttributeError, msg="Failed at {prop}"):
    self.vol.{prop} = -99
            '''
            exec(stmt)


    def test_voxel_size(self):
        '''
        Test that for every axis, the size of the pixel is correct.
        '''
        for axis in self.axes:
            stmt = f'''
self.assertAlmostEqual(self.vol.d{axis}, self.vol.{axis}pts[1] - self.vol.{axis}pts[0], msg="Failed at {axis}")
            '''
            exec(stmt)


    def test_pts_start_end(self):
        '''
        Test that for every axis, the start and end sample points are consistent with axis min, max, and wrapping.
        '''
        for axis in self.axes:
            stmt = f'''
if self.{axis}wrap:
    self.assertEqual(self.{axis}min, self.vol.{axis}pts[0], msg="{axis} start")
    self.assertEqual(self.{axis}max - self.vol.d{axis}, self.vol.{axis}pts[-1], msg="{axis} end")
else:
    self.assertAlmostEqual(self.{axis}min + self.vol.d{axis} / 2, self.vol.{axis}pts[0], msg="{axis} start")
    self.assertAlmostEqual(self.{axis}max - self.vol.d{axis} / 2, self.vol.{axis}pts[-1], msg="{axis} end")
            '''
            exec(stmt)







if __name__ == '__main__':
    unittest.main()

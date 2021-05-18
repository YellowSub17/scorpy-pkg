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

    def tearDown(self):
        pass



    def test_properties(self):
        for prop in self.properties:
            stmt = f'self.assertEqual(self.{prop}, self.vol.{prop}, msg="Failed at {prop}")'
            exec(stmt)

    def test_write_protection(self):
        for prop in self.properties:
            stmt = f'with self.assertRaises(AttributeError, msg="Failed at {prop}"):\n'
            stmt += f'\tself.vol.{prop} = -99'
            exec(stmt)


####
##  Test Properties: 
##  Ensure that inputs are correctly saved to vol with write protection 
####

    # def test_nx(self):
        # np.testing.assert_allclose(self.vol.nx, self.nx)

    # def test_nx_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.nx = -99

    # def test_ny(self):
        # np.testing.assert_allclose(self.vol.ny, self.ny)

    # def test_ny_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.ny = -99

    # def test_nz(self):
        # np.testing.assert_allclose(self.vol.nz, self.nz)

    # def test_nz_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.nz = -99

    # def test_xmax(self):
        # np.testing.assert_allclose(self.vol.xmax, self.xmax)

    # def test_xmax_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.xmax = -99

    # def test_ymax(self):
        # np.testing.assert_allclose(self.vol.ymax, self.ymax)

    # def test_ymax_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.ymax = -99

    # def test_zmax(self):
        # np.testing.assert_allclose(self.vol.zmax, self.zmax)

    # def test_zmax_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.zmax = -99

    # def test_xmin(self):
        # np.testing.assert_allclose(self.vol.xmin, self.xmin)

    # def test_xmin_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.xmin = -99

    # def test_ymin(self):
        # np.testing.assert_allclose(self.vol.ymin, self.ymin)

    # def test_ymin_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.ymin = -99

    # def test_zmin(self):
        # np.testing.assert_allclose(self.vol.zmin, self.zmin)

    # def test_zmin_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.zmin = -99

    # def test_xwrap(self):
        # np.testing.assert_allclose(self.vol.xwrap, self.xwrap)

    # def test_xwrap_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.xwrap = -99

    # def test_ywrap(self):
        # np.testing.assert_allclose(self.vol.ywrap, self.ywrap)

    # def test_ywrap_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.ywrap = -99

    # def test_zwrap(self):
        # np.testing.assert_allclose(self.vol.zwrap, self.zwrap)

    # def test_zwrap_wp(self):
        # with self.assertRaises(AttributeError):
            # self.vol.zwrap = -99



    # def test_xpts_start(self):
        # if self.vol.xwrap:
            # np.testing.assert_allclose(self.xmin, self.vol.xpts[0])
        # else:
            # np.testing.assert_allclose(self.xmin + self.vol.dx / 2, self.vol.xpts[0])





    # def test_write_protection(self):
        # '''
        # Ensure write protection of properties
        # '''
        # with self.assertRaises(AttributeError):
            # self.vol.dx = -99
        # with self.assertRaises(AttributeError):
            # self.vol.dy = -99
        # with self.assertRaises(AttributeError):
            # self.vol.dz = -99
        # with self.assertRaises(AttributeError):
            # self.vol.xpts = -99
        # with self.assertRaises(AttributeError):
            # self.vol.ypts = -99
        # with self.assertRaises(AttributeError):
            # self.vol.zpts = -99

        # with self.assertRaises(AssertionError):
            # self.vol.vol = np.ones( (self.nz, self.ny))
        # with self.assertRaises(AssertionError):
            # self.vol.vol = np.ones( (self.nz, self.nx, self.ny))

    # def test_sampling(self):
        # '''
        # Ensure sampling points are consistent with axis wrapping and sample widths
        # '''
        # np.testing.assert_allclose(self.vol.dx, self.vol.xpts[1] - self.vol.xpts[0])
        # np.testing.assert_allclose(self.vol.dy, self.vol.ypts[1] - self.vol.ypts[0])
        # np.testing.assert_allclose(self.vol.dz, self.vol.zpts[1] - self.vol.zpts[0])

        # np.testing.assert_allclose(self.xmin + self.vol.dx / 2, self.vol.xpts[0])
        # np.testing.assert_allclose(self.ymin + self.vol.dy / 2, self.vol.ypts[0])
        # np.testing.assert_allclose(self.zmin, self.vol.zpts[0])  # wrapped

        # np.testing.assert_allclose(self.xmax - self.vol.dx / 2, self.vol.xpts[-1])
        # np.testing.assert_allclose(self.ymax - self.vol.dy / 2, self.vol.ypts[-1])
        # np.testing.assert_allclose(self.zmax - self.vol.dz, self.vol.zpts[-1])  # wrapped


if __name__ == '__main__':
    unittest.main()

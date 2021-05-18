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

    def tearDown(self):
        pass

    def test_inputs(self):
        '''
        Ensure correct inputs are made and can be accessed.
        '''
        np.testing.assert_allclose(self.vol.nx, self.nx)
        np.testing.assert_allclose(self.vol.ny, self.ny)
        np.testing.assert_allclose(self.vol.nz, self.nz)

        np.testing.assert_allclose(self.vol.xmax, self.xmax)
        np.testing.assert_allclose(self.vol.ymax, self.ymax)
        np.testing.assert_allclose(self.vol.zmax, self.zmax)

        np.testing.assert_allclose(self.vol.xmin, self.xmin)
        np.testing.assert_allclose(self.vol.ymin, self.ymin)
        np.testing.assert_allclose(self.vol.zmin, self.zmin)

        np.testing.assert_allclose(self.vol.xwrap, self.xwrap)
        np.testing.assert_allclose(self.vol.ywrap, self.ywrap)
        np.testing.assert_allclose(self.vol.zwrap, self.zwrap)

    def test_write_protection(self):
        '''
        Ensure write protection of properties
        '''
        with self.assertRaises(AttributeError):
            self.vol.nx = -99
        with self.assertRaises(AttributeError):
            self.vol.ny = -99
        with self.assertRaises(AttributeError):
            self.vol.nz = -99
        with self.assertRaises(AttributeError):
            self.vol.xmax = -99
        with self.assertRaises(AttributeError):
            self.vol.ymax = -99
        with self.assertRaises(AttributeError):
            self.vol.zmax = -99
        with self.assertRaises(AttributeError):
            self.vol.xmin = -99
        with self.assertRaises(AttributeError):
            self.vol.ymin = -99
        with self.assertRaises(AttributeError):
            self.vol.zmin = -99
        with self.assertRaises(AttributeError):
            self.vol.xwrap = -99
        with self.assertRaises(AttributeError):
            self.vol.ywrap = -99
        with self.assertRaises(AttributeError):
            self.vol.zwrap = -99

        with self.assertRaises(AssertionError):
            self.vol.vol = np.ones( (self.nz, self.ny))
        with self.assertRaises(AssertionError):
            self.vol.vol = np.ones( (self.nz, self.nx, self.ny))

    def test_sampling(self):
        '''
        Ensure sampling points are consistent with axis wrapping and sample widths
        '''

        np.testing.assert_allclose(self.vol.dx, self.vol.xpts[1] - self.vol.xpts[0])
        np.testing.assert_allclose(self.vol.dy, self.vol.ypts[1] - self.vol.ypts[0])
        np.testing.assert_allclose(self.vol.dz, self.vol.zpts[1] - self.vol.zpts[0])

        np.testing.assert_allclose(self.xmin + self.vol.dx / 2, self.vol.xpts[0])
        np.testing.assert_allclose(self.ymin + self.vol.dy / 2, self.vol.ypts[0])
        np.testing.assert_allclose(self.zmin, self.vol.zpts[0])  # wrapped

        np.testing.assert_allclose(self.xmax - self.vol.dx / 2, self.vol.xpts[-1])
        np.testing.assert_allclose(self.ymax - self.vol.dy / 2, self.vol.ypts[-1])
        np.testing.assert_allclose(self.zmax - self.vol.dz, self.vol.zpts[-1])  # wrapped


if __name__ == '__main__':
    unittest.main()

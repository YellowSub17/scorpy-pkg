#!/usr/bin/env python3
import unittest

import scorpy
import numpy as np
np.random.seed(0)

import sys, os


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestSphericalVol(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.nangle = 36
        self.qmax = 1.4

        self.comp = False
        self.gridtype = 'DH1'
        self.extend = False

        self.sphv = scorpy.SphericalVol(
            self.nq, self.nangle, self.qmax, self.comp, self.gridtype, self.extend)

    def tearDown(self):
        pass

    def test_properties(self):

        self.assertEqual(self.sphv.nx, self.nq)
        self.assertEqual(self.sphv.ny, self.nangle)

        if self.gridtype == 'DH1':
            self.assertEqual(self.sphv.nz, self.nangle)
        elif self.gridtype == 'DH2':
            self.assertEqual(self.sphv.nz, 2 * self.nangle)

        self.assertEqual(self.sphv.xmax, self.qmax)
        self.assertEqual(self.sphv.ymax, np.pi / 2)
        self.assertEqual(self.sphv.zmax, 2 * np.pi)

        self.assertEqual(self.sphv.xmin, 0)
        self.assertEqual(self.sphv.ymin, -np.pi / 2)
        self.assertEqual(self.sphv.zmin, 0)
    
        self.assertEqual(self.sphv.nq, self.nq)
        self.assertEqual(self.sphv.ntheta, self.nangle)
        if self.gridtype == 'DH1':
            self.assertEqual(self.sphv.nphi, self.nangle)
        elif self.gridtype == 'DH2':
            self.assertEqual(self.sphv.nphi, 2 * self.nangle)

        self.assertEqual(self.sphv.qmax, self.qmax)

        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        self.assertEqual(self.sphv.dq, qspace[1] - qspace[0])

        thetaspace = np.linspace(-np.pi / 2, np.pi / 2,
                                 self.nangle, endpoint=False)
        np.testing.assert_allclose(
            self.sphv.dtheta, thetaspace[1] - thetaspace[0])

        if self.gridtype == 'DH1':
            phispace = np.linspace(0, 2 * np.pi, self.nangle, endpoint=False)
        elif self.gridtype == 'DH2':
            phispace = np.linspace(
                0, 2 * np.pi, 2 * self.nangle, endpoint=False)

        self.assertEqual(self.sphv.dphi, phispace[1] - phispace[0])

    # def test_saveload(self):

        # self.sphv.save(f'{test_data_dir}/tmp/sphv')
        # sphv_loaded = scorpy.PadfVol(self.nr+1, self.npsi+1, self.rmax+1, self.nl+1, self.wavelength+1,\
        # path=f'{test_data_dir}/tmp/sphv')

        # self.assertEqual(self.sphv.nx, sphv_loaded.nx)
        # self.assertEqual(self.sphv.ny, sphv_loaded.ny)
        # self.assertEqual(self.sphv.nz, sphv_loaded.nz)

        # self.assertEqual(self.sphv.xmax, sphv_loaded.xmax)
        # self.assertEqual(self.sphv.ymax, sphv_loaded.ymax)
        # self.assertEqual(self.sphv.zmax, sphv_loaded.zmax)

        # self.assertEqual(self.sphv.xmin, sphv_loaded.xmin)
        # self.assertEqual(self.sphv.ymin, sphv_loaded.ymin)
        # self.assertEqual(self.sphv.zmin, sphv_loaded.zmin)

        # self.assertEqual(self.sphv.npsi, sphv_loaded.npsi)
        # self.assertEqual(self.sphv.nr, sphv_loaded.nr)
        # self.assertEqual(self.sphv.rmax, sphv_loaded.rmax)

        # self.assertEqual(self.sphv.dr, sphv_loaded.dr)
        # self.assertEqual(self.sphv.dpsi, sphv_loaded.dpsi)

        # self.assertEqual(self.sphv.wavelength, sphv_loaded.wavelength)
        # self.assertEqual(self.sphv.nl, sphv_loaded.nl)


if __name__ == '__main__':
    unittest.main()

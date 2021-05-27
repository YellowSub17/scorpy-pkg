#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
import pyshtools as pysh
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestSphericalVol(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.ntheta = 18
        self.nphi = 36
        self.qmax = 1.4

        self.sphv = scorpy.SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)

    def tearDown(self):
        pass

    def test_inputs(self):
        '''
        Ensure correct inputs are made and can be accessed.
        '''
        np.testing.assert_allclose(self.sphv.nx, self.nq)
        np.testing.assert_allclose(self.sphv.ny, self.ntheta)
        np.testing.assert_allclose(self.sphv.nz, self.nphi)

        np.testing.assert_allclose(self.sphv.xmax, self.qmax)
        np.testing.assert_allclose(self.sphv.ymax, np.pi)
        np.testing.assert_allclose(self.sphv.zmax, 2 * np.pi)

        np.testing.assert_allclose(self.sphv.xmin, 0)
        np.testing.assert_allclose(self.sphv.ymin, 0)
        np.testing.assert_allclose(self.sphv.zmin, 0)

        np.testing.assert_allclose(self.sphv.xwrap, False)
        np.testing.assert_allclose(self.sphv.ywrap, True)
        np.testing.assert_allclose(self.sphv.zwrap, True)

    def test_properties(self):
        '''
        Ensure aliases for properties match
        '''
        np.testing.assert_allclose(self.sphv.nq, self.sphv.nx)
        np.testing.assert_allclose(self.sphv.ntheta, self.sphv.ny)
        np.testing.assert_allclose(self.sphv.nphi, self.sphv.nz)

        np.testing.assert_allclose(self.sphv.qmax, self.qmax)

    def test_pysh_sampling(self):
        q_slice = np.zeros((self.ntheta, self.nphi))
        grid_slice = pysh.SHGrid.from_array(q_slice)

        lats = -(np.radians(grid_slice.lats()) - np.pi/2)
        lons = np.radians(grid_slice.lons())

        np.testing.assert_allclose(lats, self.sphv.ypts)
        np.testing.assert_allclose(lons, self.sphv.zpts)

    # def test_sphv_to_blqq(self):

#         coeffs = np.zeros((2,self.sphv.nl, self.sphv.nl))

        # coeffs[0, 4, 1] = 1

        # sphv.set_q_coeffs(5, coeffs)

        # blqq = scorpy.BlqqVol( self.nq, self.sphv.nl, self.qmax)

        # pass

   #      qspace = np.linspace(0, self.qmax-a, self.nq, endpoint=False)
        # self.assertEqual(self.sphv.dq, qspace[1] - qspace[0])

        # thetaspace = np.linspace(-np.pi / 2, np.pi / 2,
                                 # self.nangle, endpoint=False)
        # np.testing.assert_allclose(
            # self.sphv.dtheta, thetaspace[1] - thetaspace[0])

        # if self.gridtype == 'DH1':
            # phispace = np.linspace(0, 2 * np.pi, self.nangle, endpoint=False)
        # elif self.gridtype == 'DH2':
            # phispace = np.linspace(
                # 0, 2 * np.pi, 2 * self.nangle, endpoint=False)

        # self.assertEqual(self.sphv.dphi, phispace[1] - phispace[0])

    # def test_saveload(self):

        # self.sphv.save(f'{test_data_dir}/tmp/sphv')
        # sphv_loaded = scorpy.PadfVol(self.nr+1, self.npsi+1, self.rma+1, self.nl+1, self.wavelength+1,\
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

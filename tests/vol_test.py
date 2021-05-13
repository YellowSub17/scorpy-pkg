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
        self.ny = 14
        self.nz = 6

        self.xmax = 6
        self.ymax = 2.9
        self.zmax = 180

        self.xmin = 0
        self.ymin = -2.2
        self.zmin = 0

        self.vol = scorpy.Vol(self.nx, self.ny, self.nz,
                              self.xmax, self.ymax, self.zmax,
                              self.xmin, self.ymin, self.zmin)

    def tearDown(self):
        pass

    def test_properties(self):

        self.assertEqual(self.vol.nx, self.nx)
        self.assertEqual(self.vol.ny, self.ny)
        self.assertEqual(self.vol.nz, self.nz)

        self.assertEqual(self.vol.xmax, self.xmax)
        self.assertEqual(self.vol.ymax, self.ymax)
        self.assertEqual(self.vol.zmax, self.zmax)

        self.assertEqual(self.vol.xmin, self.xmin)
        self.assertEqual(self.vol.ymin, self.ymin)
        self.assertEqual(self.vol.zmin, self.zmin)

        # qspace = np.linspace(0, self.qmax, self.nq)
        # self.assertEqual(self.corr.dq, qspace[1] - qspace[0])

        # psispace = np.linspace(0, 180, self.npsi)
        # self.assertEqual(self.corr.dpsi, psispace[1] - psispace[0])

    # def test_saveload(self):
        # self.corr.save(f'{test_data_dir}/tmp/corr')
        # corr_loaded = scorpy.CorrelationVol(self.nq + 1, self.npsi + 1, self.qmax + 1,
                                            # path=f'{test_data_dir}/tmp/corr')

        # self.assertEqual(self.corr.nx, corr_loaded.nx)
        # self.assertEqual(self.corr.ny, corr_loaded.ny)
        # self.assertEqual(self.corr.nz, corr_loaded.nz)

        # self.assertEqual(self.corr.xmax, corr_loaded.xmax)
        # self.assertEqual(self.corr.ymax, corr_loaded.ymax)
        # self.assertEqual(self.corr.zmax, corr_loaded.zmax)

        # self.assertEqual(self.corr.xmin, corr_loaded.xmin)
        # self.assertEqual(self.corr.ymin, corr_loaded.ymin)
        # self.assertEqual(self.corr.zmin, corr_loaded.zmin)

        # self.assertEqual(self.corr.nq, corr_loaded.nq)
        # self.assertEqual(self.corr.npsi, corr_loaded.npsi)
        # self.assertEqual(self.corr.qmax, corr_loaded.qmax)
        # self.assertEqual(self.corr.dq, corr_loaded.dq)
        # self.assertEqual(self.corr.dpsi, corr_loaded.dpsi)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
import unittest

import scorpy
import numpy as np
np.random.seed(0)

import sys, os


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestCorrelationVol(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.npsi = 36
        self.qmax = 1.4

        self.corr = scorpy.CorrelationVol(self.nq, self.npsi, self.qmax)

    def tearDown(self):
        pass

    def test_properties(self):

        self.assertEqual(self.corr.nx, self.nq)
        self.assertEqual(self.corr.ny, self.nq)
        self.assertEqual(self.corr.nz, self.npsi)

        self.assertEqual(self.corr.xmax, self.qmax)
        self.assertEqual(self.corr.ymax, self.qmax)
        self.assertEqual(self.corr.zmax, 180)

        self.assertEqual(self.corr.xmin, 0)
        self.assertEqual(self.corr.ymin, 0)
        self.assertEqual(self.corr.zmin, 0)
    
        self.assertEqual(self.corr.nq, self.nq)
        self.assertEqual(self.corr.npsi, self.npsi)
        self.assertEqual(self.corr.qmax, self.qmax)

        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        # TODO: why does self.nq+1, endpoint=True work?
        # qspace = np.linspace(0, self.qmax, self.nq+1)
        self.assertEqual(self.corr.dq, qspace[1] - qspace[0])

        psispace = np.linspace(0, 180, self.npsi, endpoint=False)
        # psispace = np.linspace(0, 180, self.npsi+1)
        self.assertEqual(self.corr.dpsi, psispace[1] - psispace[0])

    def test_saveload(self):
        self.corr.save(f'{test_data_dir}/tmp/corr')
        corr_loaded = scorpy.CorrelationVol(self.nq + 1, self.npsi + 1, self.qmax + 1, \
                                            path=f'{test_data_dir}/tmp/corr')

        self.assertEqual(self.corr.nx, corr_loaded.nx)
        self.assertEqual(self.corr.ny, corr_loaded.ny)
        self.assertEqual(self.corr.nz, corr_loaded.nz)

        self.assertEqual(self.corr.xmax, corr_loaded.xmax)
        self.assertEqual(self.corr.ymax, corr_loaded.ymax)
        self.assertEqual(self.corr.zmax, corr_loaded.zmax)

        self.assertEqual(self.corr.xmin, corr_loaded.xmin)
        self.assertEqual(self.corr.ymin, corr_loaded.ymin)
        self.assertEqual(self.corr.zmin, corr_loaded.zmin)

        self.assertEqual(self.corr.nq, corr_loaded.nq)
        self.assertEqual(self.corr.npsi, corr_loaded.npsi)
        self.assertEqual(self.corr.qmax, corr_loaded.qmax)
        self.assertEqual(self.corr.dq, corr_loaded.dq)
        self.assertEqual(self.corr.dpsi, corr_loaded.dpsi)


if __name__ == '__main__':
    unittest.main()

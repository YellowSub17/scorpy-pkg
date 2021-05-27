#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestCorrelationVol(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.npsi = 36
        self.qmax = 1.4

        self.corr = scorpy.CorrelationVol(self.nq, self.npsi, self.qmax)
        self.aliases = [('nx', 'nq'),
                        ('ny', 'nq'),
                        ('nz', 'npsi'),
                        ('xmax', 'qmax'),
                        ('ymax', 'qmax'),
                        ('dx', 'dq'),
                        ('dy', 'dq'),
                        ('dz', 'dpsi'),
                        ('xpts', 'qpts'),
                        ('ypts', 'qpts'),
                        ('zpts', 'psipts')]

    def tearDown(self):
        pass

    def test_aliases(self):
        for x, y in self.aliases:
            stmt = f'''
np.testing.assert_equal(self.corr.{x}, self.corr.{y}, err_msg="Fail at {x}, {y}")
            '''
            exec(stmt)

    # def test_aliases(self):

        # self.assertEqual(self.corr.nx, self.corr.nq)
        # self.assertEqual(self.corr.ny, self.corr.nq)
        # self.assertEqual(self.corr.nz, self.corr.npsi)

        # self.assertEqual(self.corr.xmax, self.corr.qmax)
        # self.assertEqual(self.corr.ymax, self.corr.qmax)
        # self.assertEqual(self.corr.zmax, 180)

        # self.assertEqual(self.corr.qmax, self.qmax)

        # self.assertEqual(self.corr.xmin, 0)
        # self.assertEqual(self.corr.ymin, 0)
        # self.assertEqual(self.corr.zmin, 0)

        # self.assertEqual(self.corr.nq, self.nq)
        # self.assertEqual(self.corr.npsi, self.npsi)
        # self.assertEqual(self.corr.qmax, self.qmax)

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

    # def test_cifdata_correl(self):
        # pass

    # def test_peakdata_correl(self):
        # pass


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
import unittest

import scorpy
import numpy as np
np.random.seed(0)

import sys, os



test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'






class TestBlqqVol(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.nl = 36
        self.qmax = 1.4

        self.blqq =  scorpy.BlqqVol(self.nq,self.nl,self.qmax)

    def tearDown(self):
        pass

    def test_properties(self):

        self.assertEqual(self.blqq.nx, self.nq)
        self.assertEqual(self.blqq.ny, self.nq)
        self.assertEqual(self.blqq.nz, self.nl)

        self.assertEqual(self.blqq.xmax, self.qmax)
        self.assertEqual(self.blqq.ymax, self.qmax)
        self.assertEqual(self.blqq.zmax, self.nl-1)

        self.assertEqual(self.blqq.xmin, 0)
        self.assertEqual(self.blqq.ymin, 0)
        self.assertEqual(self.blqq.zmin, 0)

        self.assertEqual(self.blqq.nq, self.nq)
        self.assertEqual(self.blqq.nl, self.nl)
        self.assertEqual(self.blqq.qmax, self.qmax)
        self.assertEqual(self.blqq.lmax, self.nl-1)

        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        self.assertEqual(self.blqq.dq, qspace[1]-qspace[0])



    def test_saveload(self):
        self.blqq.save(f'{test_data_dir}/tmp/blqq')
        blqq_loaded = scorpy.BlqqVol(self.nq+1, self.nl+1, self.qmax+1,\
                                     path=f'{test_data_dir}/tmp/blqq')

        self.assertEqual(self.blqq.nx, blqq_loaded.nx)
        self.assertEqual(self.blqq.ny, blqq_loaded.ny)
        self.assertEqual(self.blqq.nz, blqq_loaded.nz)

        self.assertEqual(self.blqq.xmax, blqq_loaded.xmax)
        self.assertEqual(self.blqq.ymax, blqq_loaded.ymax)
        self.assertEqual(self.blqq.zmax, blqq_loaded.zmax)

        self.assertEqual(self.blqq.xmin, blqq_loaded.xmin)
        self.assertEqual(self.blqq.ymin, blqq_loaded.ymin)
        self.assertEqual(self.blqq.zmin, blqq_loaded.zmin)

        self.assertEqual(self.blqq.nq, blqq_loaded.nq)
        self.assertEqual(self.blqq.nl, blqq_loaded.nl)
        self.assertEqual(self.blqq.qmax, blqq_loaded.qmax)
        self.assertEqual(self.blqq.lmax, blqq_loaded.lmax)
        self.assertEqual(self.blqq.dq, blqq_loaded.dq)






if __name__ == '__main__':
    unittest.main()


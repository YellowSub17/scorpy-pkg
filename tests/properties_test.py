#!/usr/bin/env python3
import unittest

import scorpy
import numpy as np
np.random.seed(0)

import sys, os


data_for_test_path = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data_for_tests'




class TestProperties(unittest.TestCase):

    def setUp(self):

        self.nq = 10
        self.npsi = 36
        self.nr = 20
        self.nl = 15
        self.qmax = 1.4
        self.rmax = 5
        self.wavelength = 2.3

    def tearDown(self):
        pass

    def test_properties_corr(self):
        corr1 = scorpy.CorrelationVol(self.nq,self.npsi,self.qmax)

        self.assertEqual(corr1.nx, self.nq)
        self.assertEqual(corr1.ny, self.nq)
        self.assertEqual(corr1.nz, self.npsi)

        self.assertEqual(corr1.xmax, self.qmax)
        self.assertEqual(corr1.ymax, self.qmax)
        self.assertEqual(corr1.zmax, 180)

        self.assertEqual(corr1.xmin, 0)
        self.assertEqual(corr1.ymin, 0)
        self.assertEqual(corr1.zmin, 0)

        self.assertEqual(corr1.npsi, self.npsi)
        self.assertEqual(corr1.nq, self.nq)
        self.assertEqual(corr1.qmax, self.qmax)



        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        self.assertEqual(corr1.dq, qspace[1]-qspace[0])

        psispace = np.linspace(0, 180, self.npsi, endpoint=False)
        self.assertEqual(corr1.dpsi, psispace[1]-psispace[0])


    def test_properties_blqq(self):
        blqq1 = scorpy.BlqqVol(self.nq,self.nl,self.qmax)

        self.assertEqual(blqq1.nx, self.nq)
        self.assertEqual(blqq1.ny, self.nq)
        self.assertEqual(blqq1.nz, self.nl)

        self.assertEqual(blqq1.xmax, self.qmax)
        self.assertEqual(blqq1.ymax, self.qmax)
        self.assertEqual(blqq1.zmax, self.nl-1)

        self.assertEqual(blqq1.xmin, 0)
        self.assertEqual(blqq1.ymin, 0)
        self.assertEqual(blqq1.zmin, 0)

        self.assertEqual(blqq1.nl, self.nl)
        self.assertEqual(blqq1.nq, self.nq)
        self.assertEqual(blqq1.lmax, self.nl-1)
        self.assertEqual(blqq1.qmax, self.qmax)

        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        self.assertEqual(blqq1.dq, qspace[1]-qspace[0])



    def test_properties_sphv(self):
        sphv1 = scorpy.BlqqVol(self.nq,self.nl,self.qmax)

        self.assertEqual(sphv1.nx, self.nq)
        self.assertEqual(sphv1.ny, self.ntheta)
        self.assertEqual(sphv1.nz, self.nphi)

        self.assertEqual(sphv1.xmax, self.qmax)
        self.assertEqual(sphv1.ymax, self.qmax)
        self.assertEqual(sphv1.zmax, self.nl-1)

        self.assertEqual(sphv1.xmin, 0)
        self.assertEqual(sphv1.ymin, 0)
        self.assertEqual(sphv1.zmin, 0)

        # self.assertEqual(sphv1.nl, self.nl)
        # self.assertEqual(sphv1.nq, self.nq)
        # self.assertEqual(sphv1.lmax, self.nl-1)
        # self.assertEqual(sphv1.qmax, self.qmax)

        qspace = np.linspace(0, self.qmax, self.nq, endpoint=False)
        self.assertEqual(blqq1.dq, qspace[1]-qspace[0])









if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python3
import unittest

import scorpy
import numpy as np
np.random.seed(0)

import sys, os


data_for_test_path = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data_for_tests'


os.system(f'rm {data_for_test_path}/tmp/*')


class TestSaveLoad(unittest.TestCase):

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

    def test_saveload_corr(self):
        corr1 = scorpy.CorrelationVol(self.nq,self.npsi,self.qmax)
        corr1.save(data_for_test_path+'/tmp/test_corr')
        corr2 = scorpy.CorrelationVol(path=data_for_test_path+'/tmp/test_corr')

        attrbs = [i for i in corr1.__dir__() if i[:2] != '__']
        for attrb in attrbs:
            if type(corr1.__getattribute__(attrb)) == type(corr1.plot_xy):
                continue
            np.testing.assert_equal(corr1.__getattribute__(attrb), corr2.__getattribute__(attrb) )

        



    def test_saveload_blqq(self):
        blqq1 = scorpy.BlqqVol(self.nq,self.nl,self.qmax)
        blqq1.save(data_for_test_path+'/tmp/test_blqq')
        blqq2 = scorpy.BlqqVol(path=data_for_test_path+'/tmp/test_blqq')


    def test_saveload_padf(self):
        padf1 = scorpy.PadfVol(self.nr, self.npsi, self.rmax, self.nl, self.wavelength)
        padf1.save(data_for_test_path+'/tmp/test_padf')
        padf2 = scorpy.PadfVol(path=data_for_test_path+'/tmp/test_padf')


    def test_saveload_sphv(self):
        sphv1 = scorpy.SphericalVol(self.nq, self.npsi, self.qmax)
        sphv1.save(data_for_test_path+'/tmp/test_sphv')
        sphv2 = scorpy.SphericalVol(path=data_for_test_path+'/tmp/test_sphv')













if __name__ == '__main__':
    unittest.main()


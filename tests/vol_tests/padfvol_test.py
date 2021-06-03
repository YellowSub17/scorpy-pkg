#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestPadfVol(unittest.TestCase):

    def setUp(self):

        self.nr = 10
        self.npsi = 36
        self.rmax = 1.4

        self.nl = 25
        self.wavelength = 2.33

        self.padf = scorpy.PadfVol(
            self.nr, self.npsi, self.rmax, self.nl, self.wavelength)

    def tearDown(self):
        pass

    def test_properties(self):
        '''
        Ensure arguments are assigned correctly
        '''

        self.assertEqual(self.padf.nx, self.nr)
        self.assertEqual(self.padf.ny, self.nr)
        self.assertEqual(self.padf.nz, self.npsi)

        self.assertEqual(self.padf.xmax, self.rmax)
        self.assertEqual(self.padf.ymax, self.rmax)
        self.assertEqual(self.padf.zmax, 1)

        self.assertEqual(self.padf.xmin, 0)
        self.assertEqual(self.padf.ymin, 0)
        self.assertEqual(self.padf.zmin, -1)

        self.assertEqual(self.padf.npsi, self.npsi)
        self.assertEqual(self.padf.nr, self.nr)
        self.assertEqual(self.padf.rmax, self.rmax)

        self.assertEqual(self.padf.wavelength, self.wavelength)
        self.assertEqual(self.padf.nl, self.nl)

        rspace = np.linspace(0, self.rmax, self.nr, endpoint=False)
        self.assertEqual(self.padf.dr, rspace[1] - rspace[0])

        psispace = np.linspace(-1, 1, self.npsi, endpoint=False)
        np.testing.assert_almost_equal(self.padf.dpsi, psispace[1] - psispace[0])

    def test_saveload(self):

        self.padf.save(f'{test_data_dir}/tmp/padf')
        padf_loaded = scorpy.PadfVol(self.nr + 1, self.npsi + 1, self.rmax + 1, self.nl + 1, self.wavelength + 1,
                                     path=f'{test_data_dir}/tmp/padf')

        self.assertEqual(self.padf.nx, padf_loaded.nx)
        self.assertEqual(self.padf.ny, padf_loaded.ny)
        self.assertEqual(self.padf.nz, padf_loaded.nz)

        self.assertEqual(self.padf.xmax, padf_loaded.xmax)
        self.assertEqual(self.padf.ymax, padf_loaded.ymax)
        self.assertEqual(self.padf.zmax, padf_loaded.zmax)

        self.assertEqual(self.padf.xmin, padf_loaded.xmin)
        self.assertEqual(self.padf.ymin, padf_loaded.ymin)
        self.assertEqual(self.padf.zmin, padf_loaded.zmin)

        self.assertEqual(self.padf.npsi, padf_loaded.npsi)
        self.assertEqual(self.padf.nr, padf_loaded.nr)
        self.assertEqual(self.padf.rmax, padf_loaded.rmax)

        self.assertEqual(self.padf.dr, padf_loaded.dr)
        self.assertEqual(self.padf.dpsi, padf_loaded.dpsi)

        self.assertEqual(self.padf.wavelength, padf_loaded.wavelength)
        self.assertEqual(self.padf.nl, padf_loaded.nl)


if __name__ == '__main__':
    unittest.main()

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



if __name__ == '__main__':
    unittest.main()

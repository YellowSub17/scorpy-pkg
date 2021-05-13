#!/usr/bin/env python3
import os
import sys
import unittest

import scorpy
import numpy as np
np.random.seed(0)


test_data_dir = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/tests/data'


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index_x(self):

        xval_ans = [(0, 0),
                    (0.001, 0),
                    (0.5, 0),

                    (1, 1),
                    (1.5, 1),

                    (2, 2),
                    (3, 3),
                    (5, 5),

                    (5.5, 5),
                    (5.999, 5),
                    (6, 5)]

        for x_val, ans in xval_ans:
            assert scorpy.utils.index_x(x_val, 0, 6, 6) == ans, f'inputs {x_val} {ans}'

        xval_ans = [(0, 0),
                    (10, 0),
                    (15, 0),

                    (16, 1),
                    (30, 1),
                    (44, 1),

                    (45, 2),
                    (60, 2),
                    (74, 2),

                    (135, 5),
                    (150, 5),
                    (164, 5),

                    (165, 0),
                    (180, 0), ]

        for x_val, ans in xval_ans:
            assert scorpy.utils.index_x(x_val, 0, 180, 6, wrap=True) == ans, f'inputs {x_val} {ans}'


if __name__ == '__main__':

    unittest.main()

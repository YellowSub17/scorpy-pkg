#!/usr/bin/env python3
import unittest
import pytest

import scorpy

import sys, os
from pathlib import Path
import numpy as np
np.random.seed(0)


data_for_test_path = Path(__file__).parent / 'data_for_tests'



class XTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass






if __name__ == '__main__':
    unittest.main()



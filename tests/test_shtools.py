import pyshtools as pysh

import numpy as np


def test_numpy_dep():

    coeffs = np.zeros( (2, 10,10))

    coeffs[0,4,3] = 1

    x = pysh.SHCoeffs().from_array(coeffs)



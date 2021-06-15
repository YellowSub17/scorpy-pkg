#!/usr/bin/env python3
'''
make-sphv.py

Make Spherical vol objects.
'''

import matplotlib.pyplot as plt
import scorpy
import numpy as np
from scorpy import __DATADIR
np.random.seed(0)




nq = 10
ntheta = 18
nphi = 36
lmax = 8
qmax = 1


sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

coeffs_key =  [ ( 0, 0, 0),
                ( 1, 2, 2),
                ( 1, 2, 1),
                ( 0, 2, 0),
                ( 0, 2, 1),
                ( 0, 2, 2),
                ( 0, 0, 0),
                ( 0, 4, 4),
                ( 1, 4, 4),
                ( 0, 4, 2),]






for q_ind, (cs, l, m) in enumerate(coeffs_key):
    coeffs = np.zeros((2, sphv.nl, sphv.nl))
    coeffs[cs, l, m] = 1
    sphv.set_q_coeffs(q_ind, coeffs)


# for q_ind in range(nq):


    # coeffs = np.zeros((2, sphv.nl, sphv.nl))
    # cs_q = np.random.randint(0, 2)
    # l_q = np.random.randint(0, 9)
    # m_l = np.random.randint(0, l_q + 1)

    # while cs_q == 1 and m_l == 0:
        # cs_q = np.random.randint(0, 2)
        # m_l = np.random.randint(0, l_q + 1)

    # coeffs[cs_q, l_q, m_l] = 1
    # print(q_ind, cs_q, l_q, m_l)

    # sphv.set_q_coeffs(q_ind, coeffs)


sphv.save(f'{__DATADIR}/dbins/sphharm_sin_sphv.dbin')

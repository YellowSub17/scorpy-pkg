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


# #### sphharm_sphv
# nq = 10
# ntheta = 18
# nphi = 36
# lmax = 8
# qmax = 1


# sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

# coeffs_key = [(0, 0, 0),
              # (1, 2, 2),
              # (1, 2, 1),
              # (0, 2, 0),
              # (0, 2, 1),
              # (0, 2, 2),
              # (0, 0, 0),
              # (0, 4, 4),
              # (1, 4, 4),
              # (0, 4, 2), ]

# for q_ind, (cs, l, m) in enumerate(coeffs_key):
    # coeffs = np.zeros((2, sphv.nl, sphv.nl))
    # coeffs[cs, l, m] = 1
    # sphv.set_q_coeffs(q_ind, coeffs)







#### fcc_sphv

nq = 100
ntheta = 180
nphi = 360



cif = scorpy.CifData(path=f'{__DATADIR}/xtal/fcc-sf.cif')
sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)


sphv.fill_from_cif(cif)

sphv.save(f'{__DATADIR}/dbins/fcc_sphv')






# ###### klnm_sphv
# nq = 100
# ntheta = 180
# nphi = 360
# lmax = 8
# qmax = 1


# sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

# def rand_coeffs():
    # cs = np.random.randint(0, 2)
    # l = np.random.randint(0, 20) * 2
    # if l == 0:
        # return (0, 0, 0)
    # if cs == 0:
        # m = np.random.randint(0, l + 1)
    # else:
        # m = np.random.randint(1, l + 1)

    # return (cs, l, m)


# for q_ind in range(nq):
    # coeffs = np.zeros((2, sphv.nl, sphv.nl))
    # cs, l, m = rand_coeffs()
    # coeffs[cs, l, m] = 1
    # sphv.set_q_coeffs(q_ind, coeffs)



# sphv.save(f'{__DATADIR}/dbins/klnm_sphv.dbin')

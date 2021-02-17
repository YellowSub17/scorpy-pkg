
import healpy as hp

import numpy as np

import matplotlib.pyplot as plt
from scipy.special import sph_harm

from scorpy.utils import ylm_wrapper



NSIDE = 2**7



theta, phi = hp.pix2ang(NSIDE, np.arange(0, hp.nside2npix(NSIDE)))


ylm = ylm_wrapper(5,2, phi, theta)
hp.orthview(ylm)
plt.title(f'L=5, m=2')



alm = hp.map2alm(ylm, lmax=6)

plt.figure()
plt.plot(alm)


plt.show()

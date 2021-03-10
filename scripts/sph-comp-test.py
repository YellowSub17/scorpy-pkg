#!/usr/bin/env python3
from scorpy.utils import ylm_wrapper
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import timeit
import healpy as hp


plt.close('all')

name = '1al1'
cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')


#get eigenvectors
bl = scorpy.BlqqVol(cor.nq, 27, cor.qmax)
bl.fill_from_corr(cor)
bl_l, bl_u = bl.get_eigh()


#make initial (target) intensities
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=cor.qmax)


Iv_init = scorpy.SphInten(cor.nq, 2**5, cor.qmax).fill_from_cif(cif)
sf = np.outer(1/np.linspace(1e-19, Iv_init.qmax, Iv_init.nq)**2, np.ones(Iv_init.npix))

#get the spherical harmonics from inital intensity
sph_init = scorpy.SphHarmHandler(cor.nq, bl.nl, cor.qmax).fill_from_ivol(Iv_init)

# filtered inten (cif -> Iv -> sph -> Iv)
Iv_filt = Iv_init.copy().fill_from_sph(sph_init)
Iv_filt.ivol *= sf

Iv_filt_sph = sph_init.copy().fill_from_ivol(Iv_filt)
Iv_filt2 = Iv_init.copy().fill_from_sph(Iv_filt_sph)
Iv_filt2.ivol *= sf



nsphere=14
Iv_init.plot_sphere(nsphere)
plt.title('I_init: Initial Intensity')

Iv_filt.plot_sphere(nsphere)
plt.title('I_filt: ivol -> sph -> ivol')

Iv_filt2.plot_sphere(nsphere)
plt.title('I_filt2: ivol -> sph -> ivol -> sph -> ivol')




plt.show()





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
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')

iv_cif = scorpy.SphInten(cor.nq, 2**5, cor.qmax).fill_from_cif(cif)
sph_cif = scorpy.SphHarmHandler(cor.nq, 57, cor.qmax).fill_from_ivol(iv_cif)

bl = scorpy.BlqqVol(cor.nq, 57, cor.qmax)
bl.fill_from_sph(sph_cif)
bl_l, bl_u = bl.get_eig()

# plt.figure()
# plt.title('Eigenvalues of Blqq filled from Spherical Harmonics, 1AL1')
# plt.plot(bl_l[-1,:])
# plt.xlabel('L')
# plt.ylabel('Eigenvalue')
# plt.show()

# assert False

plt.figure()
plt.imshow(np.log(np.abs(bl_l)+1))
plt.figure()
plt.imshow(bl_l)



###get eigenvectors
bl = scorpy.BlqqVol(cor.nq, 27, cor.qmax)
bl.fill_from_corr(cor)
bl_l, bl_u = bl.get_eig()



plt.figure()
plt.imshow(np.log(np.abs(bl_l)+1))
plt.figure()
plt.imshow(bl_l)


# assert False

# q_lin = cor.qmax*np.mgrid[0:cor.nq, 0:cor.nq, 0:bl.nl]/cor.nq
# q_lin = q_lin[0]

# bl_u[1:,1:,:] *= q_lin[1:,1:,:]**2



#make initial (target) intensities
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=cor.qmax)
Iv_init = scorpy.SphInten(cor.nq, 2**5, cor.qmax).fill_from_cif(cif)

Iv_mask = Iv_init.copy().make_mask()

#get the spherical harmonics from inital intensity
sph_init = scorpy.SphHarmHandler(cor.nq, bl.nl, cor.qmax).fill_from_ivol(Iv_init)

# filtered inten (cif -> Iv -> sph -> Iv)
Iv_filt = Iv_init.copy().fill_from_sph(sph_init)

# Calculate klnm
sph_Klnm = sph_init.copy().calc_klnm(bl_u)
# Calculate klnm'
sph_Klnmp = sph_Klnm.copy().calc_kprime(bl_l)
# Recompose Ilnm
sph_Ilmp = sph_Klnmp.copy().calc_Ilm_p(bl_u)
# k data (cif -> Iv -> sph -> klnm -> Ilm' -> Iv)
Iv_data = Iv_init.copy().fill_from_sph(sph_Ilmp)


Iv_data_masked = Iv_data.copy()
# Iv_data_masked.ivol *= Iv_mask.ivol


Iv_data2_sph = sph_init.copy().fill_from_ivol(Iv_data_masked).calc_klnm(bl_u).calc_kprime(bl_l).calc_Ilm_p(bl_u)
Iv_data2 = Iv_init.copy().fill_from_sph(Iv_data2_sph)


# relative intensity ( Iv_fil/k_data )
Iv_rela = Iv_init.copy()
Iv_rela.ivol = (Iv_filt.ivol/Iv_data.ivol)
Iv_rela.ivol[np.where(np.logical_and(Iv_filt.ivol ==0,Iv_data.ivol==0))] = 1

Iv_rela2 = Iv_init.copy()
Iv_rela2.ivol = (Iv_data2.ivol/Iv_data.ivol)
Iv_rela2.ivol[np.where(np.logical_and(Iv_data2.ivol ==0,Iv_data.ivol==0))] = 1

nsphere=75
# nsphere=84
# nsphere=88

Iv_init.plot_sphere(nsphere)
plt.title('I_init: Initial Intensity')

Iv_filt.plot_sphere(nsphere)
plt.title('Iv_filt: ivol -> Ilm -> ivol')

# Iv_rela.plot_sphere(nsphere)
# plt.title('Iv_rela: Iv_filt/Iv_data')
# Iv_rela2.plot_sphere(nsphere)
# plt.title('Iv_rela2: Iv_data2/Iv_data')


# q = np.linspace(0, cor.qmax, cor.nq)

# plt.figure()
# aves = np.mean(Iv_rela.ivol, axis=-1)
# plt.plot(q, aves)
# plt.title('Iv_filt/Iv_data')
# plt.xlabel('nq')
# plt.ylabel('Average Relative Difference')

# plt.figure()
# aves = np.mean(Iv_rela2.ivol, axis=-1)
# plt.plot(aves)
# plt.title('Iv_data2/Iv_data')
# plt.xlabel('nq')
# plt.ylabel('Average Relative Difference')



Iv_data.plot_sphere(nsphere)
plt.title('Iv_data: ivol -> Ilm -> k -> k\' -> Ilm\' -> ivol')

Iv_data2.plot_sphere(nsphere)
plt.title('Iv_data2: Iv_data -> Ilm -> k -> k\' -> Ilm\' -> ivol')

Iv_rela.plot_sphere(nsphere)
plt.title('Iv_rela: Iv_filt/Iv_data')
Iv_rela2.plot_sphere(nsphere)
plt.title('Iv_rela2: Iv_data2/Iv_data')


q = np.linspace(0, cor.qmax, cor.nq)

plt.figure()
aves = np.mean(Iv_rela.ivol, axis=-1)
plt.plot(q, aves)
plt.title('Iv_filt/Iv_data')
plt.xlabel('nq')
plt.ylabel('Average Relative Difference')

plt.figure()
aves = np.mean(Iv_rela2.ivol, axis=-1)
plt.plot(aves)
plt.title('Iv_data2/Iv_data')
plt.xlabel('nq')
plt.ylabel('Average Relative Difference')



# plt.show(block=False)
plt.show()

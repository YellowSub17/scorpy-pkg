#!/usr/bin/env python3
from scorpy.utils import ylm_wrapper
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import timeit
import healpy as hp


plt.close('all')

name = '3wct'
name = '1al1'
cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')


bl = scorpy.BlqqVol(cor.nq, 17, cor.qmax)
bl.fill_from_corr(cor)
bl_l, bl_u = bl.get_eigh()


cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=cor.qmax)
#make initial (target) and mask spherical intensities
Iv_init = scorpy.SphInten(cor.nq, 2**5, cor.qmax).fill_from_cif(cif)
#get the spherical harmonics from inital intensity
sph_init = scorpy.SphHarmHandler(cor.nq, bl.nl, cor.qmax).fill_from_ivol(Iv_init)

# filtered inten
Iv_filt = Iv_init.copy().fill_from_sph(sph_init)

# Calculate klnm
sph_Klnm = sph_init.copy().calc_klnm(bl_u)
# Recompose Ilnm
sph_Ilmp = sph_Klnm.copy().calc_Ilm_p(bl_u)
# k data
Iv_data = Iv_init.copy().fill_from_sph(sph_Ilmp)


Iv_rela = Iv_init.copy()


Iv_rela.ivol = Iv_filt.ivol/Iv_data.ivol
Iv_rela.ivol[np.where(np.logical_and(Iv_filt.ivol ==0,Iv_data.ivol==0))] = 0


# nsphere=7

# Iv_init.plot_sphere(nsphere)
# plt.title('I_init: Initial Intensity')

# Iv_filt.plot_sphere(nsphere)
# plt.title('Iv_filt: ivol -> Ilm -> ivol')

# Iv_data.plot_sphere(nsphere)
# plt.title('Iv_data: ivol -> Ilm -> k -> Ilm -> ivol')


# Iv_rela.plot_sphere(nsphere)
# plt.title('Iv_rela: Iv_filt/Iv_data')


plt.figure()
aves = np.mean(Iv_rela.ivol, axis=-1)
plt.plot(aves)
plt.title('Iv_filt/Iv_data')
plt.xlabel('nq')
plt.ylabel('Average Relative Difference')

plt.figure()
std = np.std(Iv_rela.ivol, axis=-1)
plt.plot(std)
plt.title('Error of Iv_filt/Iv_data')
plt.xlabel('nq')
plt.ylabel('Std.')

plt.figure()
sumI = np.sum(Iv_rela.ivol, axis=-1)
plt.plot(sumI)
plt.title('Diffraction Intensity over shell')
plt.xlabel('nq')
plt.ylabel('Sum Intensity')


plt.show()









# ####ned donk test
# print('\n\nNED/DONK')
# for l in range(0, sph_klnm.nl, 2):
    # ned = np.sqrt(np.abs(bl_l[:,l]))
    # donk = np.sqrt(np.sum(sph_klnm.vals_lnm[l]**2, axis=1))
    # donk[np.where(donk==0)] = 1
    # x = ned/donk
    # print(f'L={l}',f'ned=\t{ned[:3]}', f'donk=\t{donk[:3]}', f'x=\t{x[:3]}',\
          # sep='\n', end='\n\n')











# ######recon I from Klnm
# Iv_recon = Iv_mask.copy()
# Iv_recon.ivol *=0

# theta, phi = hp.pix2ang(Iv_recon.nside, np.arange(0, Iv_recon.npix))
# for l in range(0, sph_klnm.nl, 2):
    # print(l)
    # for im, m in zip(range(2*l+1), range(-l, l+1)):
        # ylm = ylm_wrapper(l,m,phi, theta, comp=False)
        # for iq in range(cor.nq):
            # bl_u_term = bl_u[:,iq,l]*sph_klnm.vals_lnm[l][:,im]
            # ylm_mesh, bl_u_mesh = np.meshgrid(ylm,bl_u_term)

            # Iv_recon.ivol += ylm_mesh*bl_u_mesh


# Iv_recon.plot_sphere(nsphere)
# plt.title('Iv_recon')

# plt.show()









# # Iv_diff = Iv_goal.copy()
# # Iv_diff.ivol = Iv_goal.ivol - Iv_filt.ivol


# # Iv_diff.plot_sphere(nsphere)
# # plt.title('I_diff: I_goal - I_filt')


# # Iv_done = Iv_goal.copy()
# # Iv_done.ivol = Iv_data.ivol + Iv_diff.ivol


# # Iv_done.plot_sphere(nsphere)
# # plt.title('I_done: I_data + I_diff')





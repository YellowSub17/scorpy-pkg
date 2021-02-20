
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import timeit


plt.close('all')

name = '1al1'
nsphere = 47


cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')


bl = scorpy.BlqqVol(cor.nq, 65, cor.qmax)
bl.fill_from_corr(cor)
bl_l, bl_u = bl.get_eigh()


cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=cor.qmax)

#make and plot the initial (target) and mask spherical intensities
Iv_goal = scorpy.SphInten(cor.nq, 2**6, cor.qmax).fill_from_cif(cif)
Iv_mask = Iv_goal.copy().make_mask()
Iv_goal.plot_sphere(nsphere)
plt.title('I_goal: Initial (and target) Intensity')


#get the spherical harmonics from inital intensity
sph_Ilm = scorpy.SphHarmHandler(cor.nq, bl.nl, cor.qmax).fill_from_ivol(Iv_goal)

#recalculate spherical intensity from harmonics and plot result
Iv_filt = Iv_goal.copy().fill_from_sph(sph_Ilm)
Iv_filt.plot_sphere(nsphere)
plt.title('I_filt: ivol -> sph -> ivol')


# #iteration steps
# sph_klmn = sph_Ilm.copy().calc_klmn(bl_u)
# sph_kpri = sph_klmn.copy().calc_kprime2(bl_l)
# sph_Ilmp = sph_kpri.copy().calc_Ilm_p(bl_u)

# Iv_data = Iv_goal.copy().fill_from_sph(sph_Ilmp)

# Iv_data.plot_sphere(nsphere)
# plt.title('I_data: ivol -> sph -> kcalc -> sph -> ivol')


# Iv_diff = Iv_goal.copy()
# Iv_diff.ivol = Iv_goal.ivol - Iv_filt.ivol


# Iv_diff.plot_sphere(nsphere)
# plt.title('I_diff: I_goal - I_filt')


# Iv_done = Iv_goal.copy()
# Iv_done.ivol = Iv_data.ivol + Iv_diff.ivol


# Iv_done.plot_sphere(nsphere)
# plt.title('I_done: I_data + I_diff')











plt.show()







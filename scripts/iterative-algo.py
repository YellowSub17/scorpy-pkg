



import scorpy
import numpy as np
import matplotlib.pyplot as plt
import timeit


plt.close('all')

name = '1al1'
ns = 6
nl = 15

cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor.dbin')
bl = scorpy.BlqqVol(cor.nq, nl, cor.qmax)

bl.fill_from_corr(cor)


print('Reading Cif.')
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=bl.qmax)
print('Done.')


iv_goal = scorpy.SphInten(100,2**ns, qmax=bl.qmax)
iv_goal.fill_from_cif(cif)

iv_mask = scorpy.SphInten(100, 2**ns, qmax=bl.qmax)
iv_mask.fill_from_cif(cif)
iv_mask.ivol[np.where(iv_mask.ivol !=0)] = 1




iv_goal.plot_sphere(80)
plt.title(f'Target Intensity, nl{nl}, nside{ns}')

iv_mask.plot_sphere(80)
plt.title(f'Mask, nl{nl}, nside{ns}')

bl_lam, bl_u = bl.get_eigh()

sph = scorpy.SphHarmHandler(bl.nq, bl.nl, bl.qmax)

sph.fill_from_ivol(iv_goal)



k_sph = sph.copy().calc_klmn2(bl_u)
# kp_sph = k_sph.calc_kprime(bl_lam)
# Ilm_p_sph = kp_sph.calc_Ilm_p(bl_u)

# iv_end = scorpy.SphInten(100,2**ns, bl.qmax)
# iv_end.fill_from_sph(Ilm_p_sph)


# iv_end.plot_sphere(80)
# plt.title(f'End Intensity, nl{nl}, nside{ns}')


# iv_end.ivol *= iv_mask.ivol
# iv_end.plot_sphere(80)
# plt.title(f'Masked End Intensity, nl{nl}, nside{ns}')

plt.show()


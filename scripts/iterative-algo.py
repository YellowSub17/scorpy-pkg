



import scorpy
import numpy as np
import matplotlib.pyplot as plt
import timeit


plt.close('all')

name = '1al1'
ns = 6
nl = 15
nsphere = 37

cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')

bl = scorpy.BlqqVol(cor.nq, nl, cor.qmax)
bl.fill_from_corr(cor)
bl_lam, bl_u = bl.get_eigh()


print('Reading Cif.')
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=cor.qmax)
print('Done.')


iv_goal = scorpy.SphInten(cor.nq, 2**ns, qmax=cor.qmax)
iv_goal.fill_from_cif(cif)
iv_goal.plot_sphere(nsphere)
plt.title(f'Target Intensity, nl{nl}, nside{ns}')


iv_mask = scorpy.SphInten(cor.nq, 2**ns, qmax=cor.qmax)
iv_mask.fill_from_cif(cif)
iv_mask.ivol[np.where(iv_mask.ivol !=0)] = 1
iv_mask.plot_sphere(nsphere)
plt.title(f'Mask, nl{nl}, nside{ns}')

# Initialize Spherical Harmonic Handler
Idatasph = scorpy.SphHarmHandler(cor.nq, nl, cor.qmax).fill_from_ivol(iv_goal)
Ifiltsph = Idatasph.copy()


Idatasph.calc_klnm(bl_u).calc_kprime(bl_lam).calc_Ilm_p(bl_u)
# Ifiltsph.calc_kprime(bl_lam).calc_Ilm_p(bl_u)
Ifiltsph.calc_klnm(bl_u).calc_Ilm_p(bl_u)

Idata = scorpy.SphInten(cor.nq, 2**ns, qmax=cor.qmax).fill_from_sph(Idatasph)
Ifilt = scorpy.SphInten(cor.nq, 2**ns, qmax=cor.qmax).fill_from_sph(Ifiltsph)

Ifilt.plot_sphere(nsphere)
plt.title('Ifilt')


# Idata.ivol += iv_goal.ivol - Ifilt.ivol


# Idata.plot_sphere(nsphere)
# plt.title('Idata')


# Idata.ivol *= iv_mask.ivol

# Idata.plot_sphere(nsphere)
# plt.title('Idata masked')

plt.show()













# (1) Calculate the klmn values from the Ilm values and bl eigenvectors
# x = Idatasph.copy().calc_klmn(bl_u)


# # Make copy of Klmn values for filtered values
# Ifiltsph = Idatasph.copy()

# # (2) Scale kprime values from klmn and bl eigenvalues
# Idatasph.calc_kprime(bl_lam)

# # (3) modify the Ilm values with the bl eigenvectors kprime values
# Idatasph.calc_Ilm_p(bl_u)
# Ifiltsph.calc_Ilm_p(bl_u)


# # (4) reconstruct intensity
# Idata = scorpy.SphInten(cor.nq,2**ns, qmax=cor.qmax)
# Idata.fill_from_sph(Idatasph)

# Ifilt = scorpy.SphInten(cor.nq,2**ns, qmax=cor.qmax)
# Ifilt.fill_from_sph(Ifiltsph)


# Idiff = iv_goal.copy()
# Idiff.ivol -= Ifilt.ivol

# Idata.ivol += Idiff.ivol


# Idata.plot_sphere(80)
# plt.title('Idata')

# Idata.ivol *= iv_mask.ivol


# Idata.plot_sphere(80)
# plt.title('Idata Masked')

# plt.show()




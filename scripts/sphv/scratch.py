
import scorpy
import matplotlib.pyplot as plt
import numpy as np
import time



nq = 100
ntheta = 180
nphi = 360


# Load cif
cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif')

# create spherical volume, fill from the cif, then get the scattering coords
sphv = scorpy.SphericalVol( nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.get_scat_sph()

sphv_scat_sph_sin = np.zeros( sphv_scat_sph.shape)
sphv_scat_sph_sin[...] = sphv_scat_sph[...]
sphv_scat_sph_sin[:,-1] *= np.sin(sphv_scat_sph[:,1])





i = 2

plt.figure()
plt.hist(sphv_scat_sph[:,i], bins=100, weights=sphv_scat_sph[:,-1], alpha=0.3, color='red')
plt.hist(cif.scat_sph[:,i], bins=100, weights=cif.scat_sph[:,-1], alpha=0.3, color='green')
plt.hist(sphv_scat_sph_sin[:,i], bins=100, weights=sphv_scat_sph_sin[:,-1], alpha=0.3, color='blue')

plt.figure()
plt.hist(sphv_scat_sph[:,i], bins=100,  alpha=0.3, color='red')
plt.hist(cif.scat_sph[:,i], bins=100,  alpha=0.3, color='green')
# plt.hist(sphv_scat_sph_sin[:,i], bins=100,  alpha=0.3, color='blue')
plt.show()




# # correlate the scattering coords from sphv
# print('corr1', time.asctime())
# corr1 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# corr1.correlate_scat_sph(sphv_scat_sph)

# # correlate the scattering coords from the cif
# print('corr2', time.asctime())
# corr2 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# corr2.fill_from_cif(cif)

# # correlate the scattering coords from sphv
# print('corr3', time.asctime())
# corr3 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# corr3.correlate_scat_sph(sphv_scat_sph_sin)

# print('finished', time.asctime())

# #plot
# corr1.plot_q1q2()
# plt.title('sphv binned')

# corr2.plot_q1q2()
# plt.title('cif')

# corr3.plot_q1q2()
# plt.title('sphv binned sin')

# plt.show()









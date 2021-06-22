
import scorpy
import matplotlib.pyplot as plt
import numpy as np
import time




nq = 10*4
ntheta = 18*4
nphi = 36*4


cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/homebrew-sf.cif', qmax=2)
corr1 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
corr1.fill_from_cif(cif, cords='scat_sph')



corr1.plot_q1q2(title='cif')
corr1.plot_sumax(title='cif')


sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.get_scat_sph()


corr2 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)

corr2.plot_q1q2(title='sphv')
corr2.plot_sumax(title='sphv')



print('sphv_scat_sph:')
print(sphv_scat_sph)

print('')

print('cif_scat_sph:')
print(cif.scat_sph)

print('')

print('bragg:')
print(cif.scat_bragg)








plt.show()










# nq = 100
# ntheta = 180
# nphi = 360




# # Load cif
# cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=15)

# # create spherical volume, fill from the cif, then get the scattering coords
# sphv = scorpy.SphericalVol( nq, ntheta, nphi, cif.qmax)
# sphv.fill_from_cif(cif)
# sphv_scat_sph = sphv.get_scat_sph()

# sphv_scat_sph_sin = np.zeros( sphv_scat_sph.shape)
# sphv_scat_sph_sin[...] = sphv_scat_sph[...]
# sphv_scat_sph_sin[:,-1] *= np.sin(sphv_scat_sph[:,1])





# i = 1

# plt.figure()
# plt.hist(sphv_scat_sph[:,i], bins=100, weights=sphv_scat_sph[:,-1], alpha=0.3, color='red', label='sphvbinned')
# plt.hist(cif.scat_sph[:,i], bins=100, weights=cif.scat_sph[:,-1], alpha=0.3, color='green', label='cif')
# plt.hist(sphv_scat_sph_sin[:,i], bins=100, weights=sphv_scat_sph_sin[:,-1], alpha=0.3, color='blue', label='sphvbinned sin')
# plt.legend()

# plt.figure()
# plt.hist(sphv_scat_sph[:,i], bins=100,  alpha=0.3, color='red', label='sphvbinned')
# plt.hist(cif.scat_sph[:,i], bins=100,  alpha=0.3, color='green', label='cif')
# plt.legend()
# plt.hist(sphv_scat_sph_sin[:,i], bins=100,  alpha=0.3, color='blue')




# # correlate the scattering coords from sphv
# corr1 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# corr1.correlate_scat_sph(sphv_scat_sph)


# # correlate the scattering coords from the cif
# corr2 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# corr2.fill_from_cif(cif)

# # correlate the scattering coords from sphv
# # corr3 = scorpy.CorrelationVol(nq, ntheta, sphv.qmax)
# # corr3.correlate_scat_sph(sphv_scat_sph_sin)

# # corr1.convolve(kern_L=2, kern_n=5, std_x=1.5, std_y=1.5, std_z=1.5)
# # corr2.convolve(kern_L=2, kern_n=5, std_x=1.5, std_y=1.5, std_z=1.5)
# # # corr3.convolve(kern_L=2, kern_n=5, std_x=1.5, std_y=1.5, std_z=1.5)

# #plot
# corr1.plot_q1q2()
# plt.title('sphv binned')
# plt.ylabel('q1q2')

# corr2.plot_q1q2()
# plt.title('cif')
# plt.ylabel('q1q2')

# # corr3.plot_q1q2()
# # plt.title('sphv binned sin')
# # plt.ylabel('q1q2')

# corr1.plot_sumax()
# plt.title('sphv binned')

# corr2.plot_sumax()
# plt.title('cif')

# # corr3.plot_sumax()
# # plt.title('sphv binned sin')

# plt.show()









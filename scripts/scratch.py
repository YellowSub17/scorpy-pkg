
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt

import scorpy







# geom = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')
# geom.plot_panels()
# pk = scorpy.PeakData(f'../data/espk/homebrew-peaks.txt', geom, cxi_flag=False, qmax=4)
# pk.plot_peaks()


# pol_points = pk.scat_pol
# pol_points[:,1] = np.degrees(pol_points[:,1])

# sph_points = pk.scat_sph
# sph_points[:,1] = np.degrees(sph_points[:,1])
# sph_points[:,2] = np.degrees(sph_points[:,2])


# print('Polar Coordinates:')
# print('\tq:\tphi:\t\tI:')
# print(pol_points)
# print()

# print('Spherical Coordinates:')
# print('\tq:\ttheta:\tphi\t\tI:')
# print(sph_points)
# print()




# corr1 = scorpy.CorrelationVol(100,180, pk.qmax)
# corr1.fill_from_peakdata(pk, method='scat_sph', verbose=False)


# corr2 = scorpy.CorrelationVol(100,180, pk.qmax)
# corr2.fill_from_peakdata(pk, method='scat_pol', verbose=False)


# corr1.plot_q1q2()
# plt.title('3D spherical q1q2')
# corr2.plot_q1q2()
# plt.title('2D Polar q1q2')

# corr1.plot_sumax()
# plt.title('3D spherical sumax')
# corr2.plot_sumax()
# plt.title('2D Polar sumax')

# plt.show()




n = 1024
seed = 0

corr1 = scorpy.CorrelationVol(path=f'../data/dbins/espk/ensemble_n{n}_{seed}.dbin')
corr2 = scorpy.CorrelationVol(path=f'../data/dbins/espk.old/ensemble_n{n}_{seed}.dbin')

corr1.plot_q1q2()
plt.title('new q1q2')
corr2.plot_q1q2()
plt.title('old q1q2')


corr_sum = scorpy.CorrelationVol(100, 180, 1.4)

for seed in range(10):
    print('seed:', seed)
    corr_seed = scorpy.CorrelationVol(path=f'../data/dbins/espk/ensemble_n1024_{seed}')

    corr_sum.vol += corr_seed.vol




extent = [corr1.psipts[5], corr1.psipts[-5], 0, corr1.qmax]
plt.figure()
plt.imshow(corr1.get_xy()[:,5:-5], origin='lower', extent=extent)
plt.title('new q1q2 (cropped)')
plt.colorbar()
plt.figure()
plt.imshow(corr2.get_xy()[:,5:-5], origin='lower', extent=extent)
plt.title('old q1q2 (cropped)')
plt.colorbar()
# plt.figure()
# plt.imshow(corr_sum.get_xy()[:,5:-5], origin='lower', extent=extent)
# plt.title('new q1q2 (cropped)')
# plt.colorbar()

# extent = [corr1.psipts[5], corr1.psipts[-5], 0, corr1.qmax]
# plt.figure()
# plt.imshow(corr1.vol.sum(axis=0)[:,5:-5], origin='lower', extent=extent)
# plt.colorbar()
# plt.figure()
# plt.imshow(corr2.vol.sum(axis=0)[:,5:-5], origin='lower', extent=extent)
# plt.colorbar()
# plt.figure()
# plt.imshow(corr_sum.vol.sum(axis=0)[:,5:-5], origin='lower', extent=extent)
# plt.colorbar()

plt.show()










# ntheta = 180
# nphi =360



# d = np.random.random( (ntheta, nphi))

# lats  = np.random.randint(-85, 85, (ntheta, nphi))
# lons  = np.random.randint(10, 350, (ntheta, nphi))




# x = pysh.expand.SHExpandLSQ(d, lats, lons, 30)[0]
# sphv = scorpy.SphericalVol(100,180,360)

# sphv.vol = np.random.random(sphv.vol.shape)
# sphv.vol[::2] =0


# lats = -1*(np.degrees(sphv.thetapts) - 90)
# lons = np.degrees(sphv.phipts)
# llons, llats = np.meshgrid(lons,lats)




# all_coeffs = []
# q_slice = sphv.vol[0]
# # if np.all(q_slice==0):
    # # pass
# # else:
# print('starting SHExpandLSQ')
# coeffs = pysh.expand.SHExpandLSQ(q_slice, llats, llons, sphv.nl)[0]
# print('done')
# all_coeffs.append(coeffs)






import numpy as np
import pyshtools as pysh

import scorpy


v = scorpy.Vol(10,6,360, 1, 180, 2*np.pi, 0, 0, 0, False, False, True)




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





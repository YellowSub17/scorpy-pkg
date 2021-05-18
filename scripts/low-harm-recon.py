import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)


sphv2 = scorpy.SphericalVol(50, 180, 360, 1)
sphv2.fill_random(lmax=8)


blqq = scorpy.BlqqVol(sphv2.nq, sphv2.nl, sphv2.qmax)
blqq.fill_from_sphv(sphv2)


sphv2.plot_slice(0, 25, extent=None)
blqq.plot_slice(2, 2, extent=None)


plt.show()


# plt.figure()
# plt.imshow(x.to_array()[0])
# plt.show()


# coeffs1 = sphv1.get_coeffs(90)
# plt.figure()
# plt.imshow(coeffs1[0])
# plt.figure()
# plt.imshow(coeffs1[1])


# sphv2 = scorpy.SphericalVol(100, 180, 360, 1)
# coeffs2 = sphv2.fill_random_sh(q=90, lmax=60)

# plt.figure()
# plt.imshow(coeffs2[0])
# plt.figure()
# plt.imshow(coeffs2[1])


# plt.show()

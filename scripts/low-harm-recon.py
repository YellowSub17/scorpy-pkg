import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)


sphv = scorpy.SphericalVol(10, 180, 360, 1)

coeffs = np.zeros((2, sphv.nl, sphv.nl))

coeffs[0, 4, 1] = 1

sphv.set_q_coeffs(5, coeffs)

blqq = scorpy.BlqqVol(sphv.nq, sphv.nl, sphv.qmax)


blqq.fill_from_sphv(sphv)


# sphv2 = scorpy.SphericalVol(50, 180, 360, 1)
# sphv2.fill_random(lmax=8)


# blqq = scorpy.BlqqVol(sphv2.nq, sphv2.nl, sphv2.qmax)
# blqq.fill_from_sphv(sphv2)


# sphv2.plot_slice(0, 30, extent=None)
# plt.title('iq=30')
# blqq.plot_slice(2, 6, extent=None)
# plt.title('l=6')
# blqq.plot_slice(2, 3, extent=None)
# plt.title('l=3')

# blqq.plot_slice(2, 5, extent=None)
# plt.title('l=5')


# plt.show()


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

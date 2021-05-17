import numpy as np
import scorpy
import matplotlib.pyplot as plt


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

sphv1 = scorpy.SphericalVol(100, 180, 360, cif.qmax)
sphv1.fill_from_cif(cif)


q_slice = sphv1.get_q_grid(90)

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

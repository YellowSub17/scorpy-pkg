import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

sphv1 = scorpy.SphericalVol(100, 180, 360, cif.qmax)
sphv1.fill_from_cif(cif)


x = sphv1.get_q_grid(90)



sphv2 = scorpy.SphericalVol(100, 180, 360, 1)
sphv2.fill_random(lmax=5)


sphv2.plot_slice(0, 10)

vol = scorpy.Vol(6,6,6,
                 180,180,180,
                 0, 0, 0,
                 True, False, False)
print(vol.xpts)
print(vol.ypts)

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

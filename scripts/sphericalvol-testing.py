import scorpy
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt


plt.close('all')

n_angle = 360
grid_type = 'DH2'
# grid_type = 'GLQ'
extend=False


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sphvol = scorpy.SphericalVol(256, n_angle,qmax=cif.qmax, grid_type=grid_type, extend=extend)

sphvol.fill_from_cif(cif)
# sphvol.convolve(kern_L=5, kern_n=19, std_x=1, std_y=1, std_z=1)



nq = 170

coeffs1 = sphvol.get_coeffs(nq)
sphvol.plot_slice(index=nq)
plt.title(f'Initial Intensity (nq={nq})')

plt.figure()
plt.imshow(coeffs1[0,...])
plt.title('coeffs init')
plt.colorbar()


sphvol.pass_filter()
coeffs2 = sphvol.get_coeffs(nq)
sphvol.plot_slice(index=nq)
plt.title(f'Filtered')

plt.figure()
plt.imshow(coeffs2[0,...])
plt.title('coeffs filtered')
plt.colorbar()



sphvol.rm_odds()
coeffs3 = sphvol.get_coeffs(nq)
sphvol.plot_slice(index=nq)
plt.title(f'rm odds')





plt.figure()
plt.imshow(coeffs3[0,...])
plt.title('coeffs rm odds')
plt.colorbar()



plt.show()

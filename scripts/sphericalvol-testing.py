import scorpy
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt


plt.close('all')

n_angle = 180
grid_type = 'DH2'
# grid_type = 'GLQ'
extend=False


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sphvol = scorpy.SphericalVol(256, n_angle,qmax=cif.qmax, grid_type=grid_type, extend=extend)

sphvol.fill_from_cif(cif)
sphvol2 = sphvol.copy()



i = 81

plt.figure()

plt.subplot(231)
sphvol.plot_slice(index=i-1, new_fig=False)
plt.title(f'Initial (nq={i-1})')
plt.colorbar()

plt.subplot(232)
sphvol.plot_slice(index=i, new_fig=False)
plt.title(f'Initial (nq={i})')
plt.colorbar()

plt.subplot(233)
sphvol.plot_slice(index=i+1, new_fig=False)
plt.title(f'Initial (nq={i+1})')
plt.colorbar()


# sphvol.convolve(kern_n=9, std_x=0.25, std_y=0.25 )

sphvol.pass_filter()

plt.subplot(234)
sphvol.plot_slice(index=i-1, new_fig=False)
plt.title(f'Filtered (nq={i-1})')
plt.colorbar()

plt.subplot(235)
sphvol.plot_slice(index=i, new_fig=False)
plt.title(f'Filtered (nq={i})')
plt.colorbar()

plt.subplot(236)
sphvol.plot_slice(index=i+1, new_fig=False)
plt.title(f'Filtered (nq={i+1})')
plt.colorbar()




plt.show()


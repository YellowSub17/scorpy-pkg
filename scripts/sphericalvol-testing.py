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

sphvol.plot_slice(index=91)
plt.title('Initial')

sphvol.pass_filter()

sphvol.plot_slice(index=91)
plt.title('Filtered')

# sphvol.rotate(2*np.pi/3,np.pi/4,np.pi/7)
sphvol.rotate(0,np.pi/6,0)

sphvol.plot_slice(index=91)
plt.title('Rotated')



plt.show()


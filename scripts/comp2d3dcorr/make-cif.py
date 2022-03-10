
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






cif = scorpy.CifData(a_mag=27.24, b_mag=31.87, c_mag=34.23, alpha=88.52, beta=108.53, gamma=111.89, spg='x')


sphv = scorpy.SphericalVol(100, 180,360, 2)
# sphv.vol = np.random.random(sphv.vol.shape)
sphv.vol +=1
cif.fill_from_sphv(sphv)


cif.save(f'{scorpy.DATADIR}/xtal/p1-intenr-sf.cif')
cif.save_hkl(f'{scorpy.DATADIR}/xtal/p1-intenr-sf.hkl')












import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






cif = scorpy.CifData(a_mag=70, b_mag=70, c_mag=70, alpha=90, beta=90, gamma=90, spg='x')


sphv = scorpy.SphericalVol(100, 180,360, 0.21)
sphv.vol +=100
cif.fill_from_sphv(sphv)


cif.save(f'{scorpy.DATADIR}/xtal/inten1-qmax021-sf.cif')
cif.save_hkl(f'{scorpy.DATADIR}/xtal/inten1-qmax021-sf.hkl')












import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






cif = scorpy.CifData(a_mag=1, b_mag=1, c_mag=1, alpha=90, beta=90, gamma=90, spg='x')


sphv = scorpy.SphericalVol(100, 180,360, 100)
sphv.vol +=1
cif.fill_from_sphv(sphv)








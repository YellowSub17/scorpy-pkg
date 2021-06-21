
import scorpy
import matplotlib.pyplot as plt
import numpy as np





sphv = scorpy.SphericalVol(path = '../data/dbins/fcc_sphv')
scat_sph = sphv.get_scat_sph()

cif = scorpy.CifData(path='../data/xtal/fcc-sf.cif')

cif._scat_sph = scat_sph














plt.show()






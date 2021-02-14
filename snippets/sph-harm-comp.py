


import scorpy
import healpy as hp
import matplotlib.pyplot as plt

# from scorpy.spharm import SphericalIntenVol


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

inten = scorpy.SphericalInten(nq=1, qmax=cif.qmax)


inten.fill_from_cif(cif)


hp.orthview(inten.ivol[0,:])

plt.show()













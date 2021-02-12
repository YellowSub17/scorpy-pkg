


import scorpy
import healpy as hp
import matplotlib.pyplot as plt

# from scorpy.spharm import SphericalIntenVol


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

inten = scorpy.SphericalIntenVol(nq=256, cifdata=cif)
hp.orthview(inten.ivol[100])

sph = inten.calc_sph(65)

inten = sph.calc_ivol(inten.nside)
hp.orthview(inten.ivol[100])




plt.show()





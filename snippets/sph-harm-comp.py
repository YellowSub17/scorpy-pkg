


import scorpy
import healpy as hp
import matplotlib.pyplot as plt

# from scorpy.spharm import SphericalIntenVol



nq=100
nl=23
qmax=0.35


cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax=qmax)

inten1 = scorpy.SphInten(nq=nq, qmax=qmax)
inten1.fill_from_cif(cif)
hp.orthview(inten1.ivol[50,:])



sph = scorpy.SphHarmHandler(nq=nq, nl=nl,qmax=qmax)

sph.fill_from_cif(cif)

inten2 = scorpy.SphInten(nq=nq, qmax=qmax)
inten2.fill_from_sphharmhandler(sph)

hp.orthview(inten2.ivol[50,:])




plt.show()













import scorpy
import numpy as np
import matplotlib.pyplot as plt
from scorpy.env import __DATADIR




cif = scorpy.CifData(f'{__DATADIR}/xtal/fcc-sf.cif')

sphv = scorpy.SphericalVol(100, 180, 360, cif.qmax)

iqlm =  scorpy.IqlmHandler(100, 90, cif.qmax)
iqlm.fill_from_sphv(sphv)





print('filling blqq')
blqq = scorpy.BlqqVol(sphv.nq, sphv.nl, sphv.qmax)
blqq.fill_from_iqlm(sphv)


lams, us = blqq.get_eig()


print('filling ilm')
klnm1 = scorpy.KlnmHandler(sphv.nl, sphv.nq, sphv.qmax)
klnm1.fill_ilm(sphv)


print('filling klnm')
klnm2 = klnm1.copy()
klnm2.fill_klnm(us)


print('filling kprime')
klnm3 = klnm2.copy()
klnm3.fill_kprime(lams)


print('filling ilmprime')
klnm4 = klnm3.copy()
klnm4.fill_ilmprime(us)







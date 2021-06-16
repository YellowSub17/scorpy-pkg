import scorpy
import numpy as np
import matplotlib.pyplot as plt


sphv1 = scorpy.SphericalVol(path='../data/dbins/klnm_sphv')

blqq = scorpy.BlqqVol(sphv1.nq, sphv1.nl, sphv1.qmax)
blqq.fill_from_sphv(sphv1)


lams, us = blqq.get_eig()


klnm1 = scorpy.KlnmHandler(sphv1.nl, sphv1.nq, sphv1.qmax)

klnm1.fill_ilm(sphv1)


klnm2 = klnm1.copy()

klnm2.fill_klnm(us)

klnm3 = klnm2.copy()
klnm3.fill_kprime(lams)


klnm4 = klnm3.copy()
klnm4.fill_ilmprime(us)


sphv1

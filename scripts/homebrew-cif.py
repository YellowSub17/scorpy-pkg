import numpy as np
import scorpy
import matplotlib.pyplot as plt







cif = scorpy.CifData('../data/xtal/homebrew-sf.cif')

qmax = cif.qmax+0.1*cif.qmax
nq=20
ntheta=36
nl = 17

cor1 = scorpy.CorrelationVol(nq=nq, ntheta=ntheta, qmax=qmax)
cor1.correlate(cif.scattering)



bl1 = scorpy.BlqqVol(nq, nl, qmax)
bl1.fill_from_corr(cor1)

bl1l, bl1u = bl1.get_eig()


sph1 = scorpy.SphHarmHandler(nq, nl, qmax)
sph1.fill_from_cif(cif)

bl2 = scorpy.BlqqVol(nq,nl,qmax)
bl2.fill_from_sph(sph1)
bl2l, bl2u = bl2.get_eig()

bl_rel = bl1.copy()
bl_rel.vol[np.where(bl2.vol !=0)] /= bl2.vol[np.where(bl2.vol !=0)]









cor1.plot_sumax()
plt.title('correlation (sum)')

cor1.plot_q1q2()
plt.title('correlation (q1q2)')




cor1.plot_slice(2,0)
plt.title('cor theta=0')
cor1.plot_slice(2,-1)
plt.title('cor theta=180')

l = 0
bl1.plot_slice(2,l)
plt.title('blqq1 from cor (l=0)')
bl2.plot_slice(2,l)
plt.title('blqq2 from sph (l=0)')

bl_rel.plot_slice(2,l)
plt.title('blqq rel (l=0)')




plt.show()


import scorpy
import matplotlib.pyplot as plt
import numpy as np
import time




nq = 100
ntheta = 180
nphi = ntheta*2

npsi = 180

cif = scorpy.CifData(path=f'{scorpy.__DATADIR}/xtal/fcc-sf.cif', qmax=20)
corr1 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr1.fill_from_cif(cif, method='scat_sph')



corr1.plot_q1q2(title='cif q1q2')
plt.axis([-1,1,10, 18])
# plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/sphv-comp-cifq1q2.png')
corr1.plot_sumax(title='cif sumq')
plt.axis([-1,1,10, 18])
# plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/sphv-comp-cifsumq.png')


sphv = scorpy.SphericalVol(nq, ntheta, nphi, cif.qmax)
sphv.fill_from_cif(cif)
sphv_scat_sph = sphv.ls_pts()

corr2 = scorpy.CorrelationVol(nq,npsi, cif.qmax)
corr2.correlate_scat_sph(sphv_scat_sph)

corr2.plot_q1q2(title='sphv q1q2')
plt.axis([-1,1,10, 18])
# plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/sphv-comp-sphvq1q2.png')
corr2.plot_sumax(title='sphv sumq')
plt.axis([-1,1,10, 18])
# plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/sphv-comp-sphvsumq.png')


plt.show()







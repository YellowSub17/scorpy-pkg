
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



# nr = 1500
# npsi = 90

# nl = 6
# wavelength = 1.33
sim_n = 2048


# # sf = 2*np.pi
# sf = 1/2*np.pi

# qmax = 1.45*sf #A-1
# nq = 100
# # dq = np.abs(qmax / nq)






# wavelength = 6.7018e-11*1e10
# qmax = 3.70153e+09
# rmax = 8.64506e-09



# qmax = 1.45/(2*np.pi)
# dq = qmax/nq
# rmax = 1/dq
# print(f'{rmax=}')



rmax = 86/2
wavelength = 6.7018e-11*1e10
npsi_q = 180
npsi_r = 90
sf = 1/(2*np.pi)

nq = 100
nr = 200
nl = 32




for part in ['p0', 'p1']:


    padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-{part}-padf.dbin'
    corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-{part}-qcor.dbin'

    # corr = scorpy.CorrelationVol(path=corr_path)

    # # # # corr = scorpy.CorrelationVol(nq, npsi_q, qmax, cos_sample=False)
    # # # # corr.vol = np.random.random(corr.vol.shape)

    # padf = scorpy.PadfVol(nr=nr, npsi=npsi_r, rmax=rmax, nl=nl, wavelength=wavelength)
    # padf.fill_from_corr(corr, theta0=False, verbose=99, tag=part)
    # padf.save(padf_path)


#+\-3.e46


    padf = scorpy.PadfVol(path=padf_path)
    padf.plot_r1r2()

plt.show()







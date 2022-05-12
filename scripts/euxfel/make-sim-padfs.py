
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






wavelength = 6.7018e-11*1e10
qmax = 3.70153e+09
rmax = 8.64506e-09
npsi_q = 402
nq = 128
nr= 128
nl=4

sf = 1/(2*np.pi)



# corr1_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p0-qcor.dbin'
padf1_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p0-padf-x.dbin'

# corr2_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p1-qcor.dbin'
# padf2_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p1-padf-x.dbin'



# corr1 = scorpy.CorrelationVol(path=corr1_path)

corr1 = scorpy.CorrelationVol(nq, npsi_q, qmax, cos_sample=False)
corr1.vol = np.random.random(corr1.vol.shape)

padf1 = scorpy.PadfVol(nr=nr, npsi=npsi_q, rmax=rmax, nl=nl, wavelength=wavelength)
padf1.fill_from_corr(corr1, theta0=False, verbose=99, sf=sf, tag='p1')
padf1.save(padf1_path)

# corr2 = scorpy.CorrelationVol(path=corr2_path)
# padf2 = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)
# padf2.fill_from_corr(corr2, theta0=False, verbose=99, sf=sf, tag='p2')
# padf2.save(padf2_path)




# padf1 = scorpy.PadfVol(path=padf1_path)
# corr1 = scorpy.CorrelationVol(path=corr1_path)

# padf2 = scorpy.PadfVol(path=padf2_path)
# corr2 = scorpy.CorrelationVol(path=corr2_path)




# # padf1._rmax = np.pi*padf1.rmax
# # padf2._rmax = np.pi*padf2.rmax

# corr1.vol[:,:,0] = 0
# corr2.vol[:,:,0] = 0

# # padf1 = padf1.crop(0, 0, 0, 50, 50, 89)
# # padf2 = padf2.crop(0, 0, 0, 50, 50, 89)
# # padf1 = padf1.crop(0, 0, 0, 100, 100, 89)
# # padf2 = padf2.crop(0, 0, 0, 100, 100, 89)




# for ir, r in enumerate(padf1.xpts):
    # print(ir, r)

# vminmax = (-5e67, 7.5e67)


# fig, axes = plt.subplots(1,2)
# padf1.plot_xy(vminmax=vminmax, xlabel='psi [rad]', ylabel='r1=r2 [A]', title='padf1 wo. theta0',fig=fig,axes=axes[0])
# padf2.plot_xy(vminmax=vminmax, xlabel='psi [rad]', ylabel='r1=r2 [A]', title='padf2 wo. theta0',fig=fig,axes=axes[1])



# rr = 18
# rr = 25
# rr = 28

# plt.figure()
# plt.plot(padf1.get_xy()[rr,:])
# plt.plot(padf2.get_xy()[rr,:])



# corr1.plot_q1q2( xlabel='psi [rad]', ylabel='q1=q2 [A]', title='corr1 wo. theta0')
# corr2.plot_q1q2( xlabel='psi [rad]', ylabel='q1=q2 [A]', title='corr2 wo. theta0')



plt.show()







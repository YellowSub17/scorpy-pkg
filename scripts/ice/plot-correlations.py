
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')









corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
# corr3d.vol[:,:,:10] = 1
# corr3d.vol[:,:,-10:] = 1

# fig, ax = plt.subplots(1,1,)
# corr3d.plot_sumax(0, log=False, title='3D structure factors Sum', fig=fig, axes=ax, extent=[0, 180, corr3d.qmin, corr3d.qmax])


fig, ax = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi= 300)
corr3d.plot_q1q2(log=True, title='3D structure factors q1q2', fig=fig, axes=ax, extent=[0, 180, corr3d.qmin, corr3d.qmax])
plt.savefig('/home/pat/Documents/phd/figs/py/ice_3d_q1q2.png')

# fig, ax = plt.subplots(1,1,)
# corr3d.convolve(kern_L= 3, kern_n=9,)
# corr3d.plot_q1q2(log=False, title='3D structure factors blurred', fig=fig, axes=ax, extent=[0, 180, corr3d.qmin, corr3d.qmax])

# fig, ax = plt.subplots(1,1,)
# corr3d.plot_sumax(0, log=False, title='3D structure factors Sum Blurred', fig=fig, axes=ax, extent=[0, 180, corr3d.qmin, corr3d.qmax])




corr3d.convolve()


fig, ax = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi= 300)
corr3d.plot_slice(2, 59, title=f'{np.degrees(corr3d.psipts[59])} degrees', xlabel='q1', ylabel='q2', fig=fig, axes=ax )
plt.savefig('/home/pat/Documents/phd/figs/py/ice_3dcorr_59deg.png')

fig, ax = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi= 300)
corr3d.plot_slice(2, 89, title=f'{np.degrees(corr3d.psipts[89])} degrees', xlabel='q1', ylabel='q2', fig=fig, axes=ax)
plt.savefig('/home/pat/Documents/phd/figs/py/ice_3dcorr_89deg.png')







size = '125nm'

stds = [-99900 ]
stds += [i for i in range(0, 351, 25)]


# # stds = [-99900,0 ]

# # stds = [i for i in range(0, 51, 25)]



# stds = [i for i in range(0, 151, 25)]

corra = corr3d.copy()
corrb = corr3d.copy()

corra.vol *=0
corrb.vol *=0

apple = []

for i, std in enumerate(stds[:-1]):
    c1 = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std{std}-{stds[i+1]}-a-qcor.dbin')
    c2 = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std{std}-{stds[i+1]}-b-qcor.dbin')

    corra.vol +=c1.vol
    corrb.vol +=c2.vol

    corra.vol[:,:, :5] = 0
    corrb.vol[:,:, :5] = 0


#     corrac = corra.copy()
    # corrbc = corrb.copy()

    # corrac.convolve()
    # corrbc.convolve()

    print(std, stds[i+1], scorpy.utils.utils.cosinesim(corra.vol, corrb.vol))
    # print('c', std, stds[i+1], scorpy.utils.utils.cosinesim(corrac.vol, corrbc.vol))
    print()

    apple.append(scorpy.utils.utils.cosinesim(corra.vol, corrb.vol))


# corr3d.plot_q1q2(title='3d', xlabel='$\\Delta\\Psi$ [rad]', ylabel='q [A-1]')
# corra.convolve()

corra.vol +=corrb.vol


fig, ax = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi= 300)
corra.plot_q1q2(vminmax=(0,26471023910), title='Simulated',extent=[0, 180, corr3d.qmin, corr3d.qmax], fig=fig, axes=ax)
plt.tight_layout()
# corrb.convolve()
# corrb.plot_q1q2()
# plt.tight_layout()

plt.savefig('/home/pat/Documents/phd/figs/py/ice_simulated_q1q2.png')








plt.show()























import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.close('all')




# fnames = ['inten1-qmax0264-2d-ssph-batch-noint-noselfcorr-qcor',
    # 'inten1-qmax0264-2d-ssph-batch-noint-selfcorr-qcor',
    # 'inten1-qmax0264-2d-ssph-batch-int-noselfcorr-qcor',
    # 'inten1-qmax0264-2d-ssph-batch-int-selfcorr-qcor']



# fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
# plt.suptitle('2D (crop highlow theta)')
# for i, fname in enumerate(fnames):
    # corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/{fname}.dbin')
    # corr.vol[:,:,:20] = 0
    # corr.vol[:,:,-20:] = 0
    # corr.plot_q1q2(title=f'{fname[30:]}', fig=fig, axes=axes.flatten()[i])


# fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
# plt.suptitle('2D (no crop)')
# for i, fname in enumerate(fnames):
    # corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/{fname}.dbin')
    # corr.plot_q1q2(title=f'{fname[30:]}', fig=fig, axes=axes.flatten()[i])




corr3d = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-3d-sph-selfcorr-qcor.dbin')
corr2d =  scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-2d-ssph-batch-int-selfcorr-qcor.dbin')

corr2d.vol[:,:,:5] = 0
corr2d.vol[:,:,-5:] = 0
corr3d.vol[:,:,:5] = 0
corr3d.vol[:,:,-5:] = 0

corr3d.plot_q1q2(title=f'3D')
corr2d.plot_q1q2(title=f'2D')
corr2d.plot_q1q2(log=True, title=f'2D log')


# inte_rq = 0.0075
# inte_rt = np.pi/64

inte_rq = 0.0100
inte_rt = np.pi/40





rect = patches.Rectangle((np.pi/2 -inte_rt, 0.2020-inte_rq), inte_rt*2, inte_rq*2, 0,
                         fill=False, ec='red', alpha=1, lw=1)
plt.gca().add_patch(rect)



corr2d_inte = corr2d.copy()
corr2d_inte.vol *=0

corr3d_inte = corr2d.copy()
corr3d_inte.vol *=0



for point, inds in zip(corr3d.ls_pts(), corr3d.ls_pts(inds=True)):
    s, loc = corr2d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
    npixforthispeak = len(np.where(corr2d.vol[loc]>0)[0])
    corr2d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s#/npixforthispeak

    s, loc = corr3d.integrate_region(point[0], point[1], point[2], inte_rq, inte_rq, inte_rt)
    npixforthispeak = len(np.where(corr3d.vol[loc]>0)[0])
    corr3d_inte.vol[int(inds[0]), int(inds[1]), int(inds[2])] = s#/npixforthispeak




corr2d_inte.plot_q1q2(title='2d integrated')
corr3d_inte.plot_q1q2(title='3d integrated')




qq = 76

plt.figure()
plt.plot(corr3d.psipts, corr3d.vol[qq, qq,:])
plt.title('corr3d')

plt.figure()
plt.plot(corr3d_inte.psipts, corr3d_inte.vol[qq, qq,:])
plt.title('corr3d_inte')


plt.figure()
plt.plot(corr2d.psipts, corr2d.vol[qq, qq,:])
plt.title('corr2d')

plt.figure()
plt.plot(corr2d_inte.psipts, corr2d_inte.vol[qq, qq,:])
plt.title('corr2d_inte')








plt.show()



import scorpy
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab




corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')

corr3d.qpsi_correction()
xyzi = corr3d.ls_pts()
# figure = mlab.figure('corr3d pts')
# mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2],xyzi[:,3] , scale_mode='none', scale_factor=0.1)
# mlab.axes(xlabel='q1', ylabel='q2', zlabel='psi',ranges=(1.5, 3.1, 1.5, 3.1, 0, np.pi))







# corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
# print(corr3d.qmax, corr3d.qmin, corr3d.cos_sample)
# corr3d.convolve(kern_n=17, kern_L=5, std_x=2, std_y=2, std_z=2)
# figure = mlab.figure('corr3d')
# mlab.axes(xlabel='q1', ylabel='q2', zlabel='psi',ranges=(1.5, 3.1, 1.5, 3.1, 0, np.pi))
# mlab.contour3d(corr3d.vol)


corra = corr3d.copy()
corrb = corr3d.copy()
corra.vol *=0
corrb.vol *=0


stds = [-99900 ]
stds += [i for i in range(0, 351, 25)]

size='125nm'
for i, std in enumerate(stds[:-1]):
    c1 = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std{std}-{stds[i+1]}-a-qcor.dbin')
    c2 = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std{std}-{stds[i+1]}-b-qcor.dbin')


    corra.vol +=c1.vol
    corrb.vol +=c2.vol

    corra.vol[:,:, :5] = 0
    corrb.vol[:,:, :5] = 0


corra.vol +=corrb.vol



xx, yy, zz = np.mgrid[1.5:3.1:100j, 1.5:3.1:100j, 0:np.pi:180j]


# f = mlab.figure('c')
# mlab.contour3d(xx, yy, zz, corra.vol, figure=f)
# mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2], extent=[1.5,3.1, 1.5, 3.1, 0, np.pi],scale_mode='none', scale_factor=0.1, figure=f)
# mlab.axes()







f = mlab.figure('c', bgcolor=(0,0,0) )
mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2], extent=[1.5,3.1, 1.5, 3.1, 0, np.pi], color=(1,0,0), scale_mode='none', scale_factor=0.1, figure=f)


xyzi= corra.ls_pts()

# plt.figure()
# plt.hist(np.log10(xyzi[:,-1]+1), bins=250)
# plt.show()




xyzi= corra.ls_pts(thresh=1e11)
mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2], extent=[1.5,3.1, 1.5, 3.1, 0, np.pi],color=(1,1,1), opacity=0.1, scale_mode='none', scale_factor=0.1, figure=f)



# f = mlab.figure('c')
# mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2], xyzi[:,3], extent=[1.5,3.1, 1.5, 3.1, 0, np.pi],scale_mode='none', scale_factor=0.1, figure=f)
# xyzi= corra.ls_pts(thresh=1e15)
# mlab.points3d(xyzi[:,0],xyzi[:,1],xyzi[:,2], xyzi[:,3], extent=[1.5,3.1, 1.5, 3.1, 0, np.pi],scale_mode='none', scale_factor=0.1, figure=f)



mlab.show()




import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')




# corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/inten1-qmax0264-3d-sph-selfcorr-qcor.dbin')




# corr = scorpy.CorrelationVol(100, 100, 100, cos_sample=True)


nx = 100
xmax = 100


corr = scorpy.Vol(nx,nx,nx, 0, 0,0, xmax,xmax,xmax)


corr.vol[0,0,0] = 1
corr.vol[-1,-1,-1] = 1



corr.vol[10, 5, 60] = 1
corr.vol[12, 7, 62] = 1
corr.vol[8, 3, 58] = 1




fig = plt.figure()
ax = plt.axes(projection ='3d')
xyzi = corr.ls_pts()
ax.scatter( xyzi[:,0], xyzi[:,1], xyzi[:,2])
plt.xlabel('x')
plt.ylabel('y')



out, loc = corr.integrate_region( 10, 5, 60, 10, 10, 10)


corr.vol[loc] +=1




fig = plt.figure()
ax = plt.axes(projection ='3d')
xyzi = corr.ls_pts()
ax.scatter( xyzi[:,0], xyzi[:,1], xyzi[:,2], c=xyzi[:,-1])
plt.xlabel('x')
plt.ylabel('y')









# out = corr.integrate_peaks()













plt.show()






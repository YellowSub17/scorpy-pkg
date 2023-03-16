
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')












corr3d = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')
corra = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-1000nm-19MPz18-a-qcor.npy')
corrb = scorpy.CorrelationVol(path='/media/pat/datadrive/ice/sim/corr/hex-ice-1000nm-19MPz18-b-qcor.npy')

# corrc = corra.copy()

corr3d.vol[:,:, :10] = 0
corr3d.vol[:,:, -10:] = 0
corra.vol[:,:, :10] = 0
corrb.vol[:,:, :10] = 0



corra.qpsi_correction()
corrb.qpsi_correction()

# corr3d.plot_q1q2(vminmax=(0, 1e6))
# kern = corr3d.convolve_tophat(kern_n=9, kern_L=1.1, lim_x=1, lim_y=1, lim_z=0)
# kern = corr3d.convolve(kern_n=9, kern_L=1.1, std_x=1, std_y=1, std_z=0)
# kern = corr3d.convolve()
# plt.figure()
# plt.imshow(kern[:,:,4])
corr3d.plot_q1q2(log=True)

# kern = corra.convolve_tophat(kern_n=5, kern_L=1.1, lim_x=1, lim_y=1, lim_z=0)
corra.plot_q1q2(log=True)
# kern = corrb.convolve_tophat(kern_n=5, kern_L=1.1, lim_x=1, lim_y=1, lim_z=0)
corrb.plot_q1q2(log=True)

# corrc.vol =corra.vol +corrb.vol
# corrc.plot_q1q2(vminmax=(0, 1e14))






q1, q2, q3 = corra.get_index(x=1.6), corra.get_index(x=1.72), corra.get_index(x=1.815),
q4 = corra.get_index(x=2.34)
q5, q6, q7 = corra.get_index(x=2.77), corra.get_index(x=2.9), corra.get_index(x=3.025),

plt.figure()
q = q3
plt.plot(corra.vol[q, q,:]/np.max(corra.vol[q,q,:]))
plt.plot(corr3d.vol[q, q,:]/np.max(corr3d.vol[q,q,:]))







plt.show()

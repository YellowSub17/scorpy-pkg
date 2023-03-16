import numpy as np
import scorpy
import os
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')




# pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/hex-ice-x1.h5',
            # geompath='/media/pat/datadrive/ice/sim/geoms/19MPz18.geom')

# pk.plot_peaks()

# pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/hex-ice-x2.h5',
            # geompath='/media/pat/datadrive/ice/sim/geoms/19MPz18.geom')

# pk.plot_peaks()






# chunk = np.random.randint(0, 9)
# frame = np.random.randint(1, 1000)
# pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/14MP/hex-ice-250nm-14MP-{chunk}-{frame}.npz',
            # geompath='/media/pat/datadrive/ice/sim/geoms/14MP.geom')

# pk.plot_peaks()
# pk.plot_qring(1.4)






# im = np.zeros( (2800, 2800) )

# for chunk in range(1):
    # print(chunk)
    # for i in range(1,1001):

        # pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/agipdv2/hex-ice-250nm-agipdv2-{chunk}-{i}.npz',
                    # geompath='/media/pat/datadrive/ice/sim/geoms/agipdv2.geom')

        # im += pk.make_im(2800, 0.14)

# plt.figure()
# plt.imshow(im)


# pk.plot_peaks()
# pk.plot_qring(1.6)


# patterns_glob = glob.glob(f'/media/pat/datadrive/ice/sim/patterns/19MPz18/*250nm*.npz')
# pk = scorpy.PeakData(datapath=patterns_glob[:500],
                    # geompath='/media/pat/datadrive/ice/sim/geoms/19MPz18.geom')


# im = pk.make_im(1400, 0.127)
# plt.figure()
# plt.imshow(im, origin='lower')



# patterns_glob = glob.glob(f'/media/pat/datadrive/ice/sim/patterns/19MPz18/*500nm*.npz')
# pk = scorpy.PeakData(datapath=patterns_glob[:500], 
                    # geompath='/media/pat/datadrive/ice/sim/geoms/19MPz18.geom')


# im = pk.make_im(1400, 0.127)
# plt.figure()
# plt.imshow(im, origin='lower')




# patterns_glob = glob.glob(f'/media/pat/datadrive/ice/sim/patterns/19MPz18/100nm/*100nm*.npz')
# pk = scorpy.PeakData(datapath=patterns_glob,
                    # geompath='/media/pat/datadrive/ice/sim/geoms/19MPz18.geom')


# im = pk.make_im(1000, 0.127)
# plt.figure()
# plt.imshow(im, origin='lower')
# plt.title('100nm')













# pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/14MP/hex-ice-250nm-14MP-0-40.npz',
            # geompath='/media/pat/datadrive/ice/sim/geoms/14MP.geom')

# # inte = pk.integrate_peaks(0.005)
# # pk.calc_scat(inte[:,0:3], inte[:,-1])
# pk.plot_peaks()
# pk.plot_peakr(0.005)
# pk.plot_qring(2)
# pk.plot_qring(2.25)
# pk.plot_qring(3.29)
# pk.plot_qring(3.80)







# corra.plot_q1q2( title='corra')
# corrb.plot_q1q2(title='corrb')

# # corra.plot_q1q2(vminmax=(0, 1e9), title='corra')
# # corrb.plot_q1q2(vminmax=(0, 1e9), title='corrb')

# q145 =  corra.get_index(x = 1.45)


# q145Ia = corra.vol[q145, q145, :]
# q145Ib = corrb.vol[q145, q145, :]
# plt.figure()
# plt.plot(q145Ia[5:]/np.max(q145Ia[5:]))
# plt.plot(q145Ib[5:]/np.max(q145Ib[5:]))





# pk = scorpy.PeakData(datapath=f'/media/pat/datadrive/ice/sim/patterns/agipd/hex-ice-1um-agipd-{1}-{1}.npz',
            # geompath='/media/pat/datadrive/ice/sim/geoms/agipd_v1.geom')
# pk.plot_peaks()
# pk.plot_qring(1.6)




plt.show()







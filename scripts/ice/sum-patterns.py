

import numpy as np
import scorpy
import os
import h5py

import glob
import sys
from datetime import datetime

import matplotlib.pyplot as plt
plt.close('all')




geom =  '19MPz18'


size = sys.argv[1]

part = sys.argv[2]


std_sf1 = float(sys.argv[3])
std_sf2 = float(sys.argv[4])



corr_means = np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-means.npy')
corr_sq_means =np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-sq-means.npy')


xs = np.sqrt(  corr_means**2 - corr_sq_means   )
xs_log = np.log10(xs)

xs_log_counts, xs_log_bins = np.histogram(xs_log, bins=1000)
xs_log_mean = xs_log.mean()
xs_log_std = xs_log.std()
xs_log_median = np.median(xs_log)


xs_log_mode_loc = int(np.where(xs_log_counts==np.max(xs_log_counts))[0][0])
xs_log_mode = xs_log_bins[xs_log_mode_loc]

xs_thresh_lower = xs_log_mode+xs_log_std*std_sf1
xs_thresh_upper = xs_log_mode+xs_log_std*std_sf2


cond1 = xs_log > xs_thresh_lower
cond2 = xs_log <= xs_thresh_upper


chunk_is, pattern_is= np.where(np.logical_and(cond1, cond2))


if part=='a':
    if len(chunk_is) %2 ==0:
        chunk_is = chunk_is[::2]
        pattern_is = pattern_is[::2]
    else:
        chunk_is = chunk_is[:-1:2]
        pattern_is = pattern_is[:-1:2]
else:
    chunk_is = chunk_is[1::2]
    pattern_is = pattern_is[1::2]





print(f'<{datetime.now().strftime("%H:%M:%S")}>')
print(f'\tSumming patterns for {size}')
print(f'\tstd {std_sf1} to {std_sf2}')
print(f'\tSumming {len(chunk_is)} patterns for part {part.capitalize()}')


im = np.zeros((1000,1000))
pk_list = []
for i,  (chunk_i, pattern_i) in  enumerate(zip(chunk_is, pattern_is)):

    print(i, end='\r')


    pk = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-{chunk_i+1}-{pattern_i+1}.npz',
                             geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')

    inte = pk.integrate_peaks(0.005)

    pk.calc_scat(inte[:,0:3], inte[:,-1])

    im += pk.make_im(1000, 0.127)


np.save(f'/media/pat/datadrive/ice/sim/patterns/sums/hex-ice-{size}-std{int(std_sf1*100)}-{int(std_sf2*100)}-{part}', im)









# # sizes = ['500nm', '1000nm']
# sizes = ['125nm']
# geom = '19MPz18'

# for size in sizes:

    # patterns_path = f'/media/pat/datadrive/ice/sim/patterns/{geom}/{size}/*{size}*.npz'
    # print(patterns_path)
    # patterns_glob = glob.glob(patterns_path)
    # patterns_glob.sort()



    # if int(sys.argv[1]) ==0:
        # start = 0
        # end = 10000
    # elif int(sys.argv[1])==1:
        # start = 10000
        # end = 20000

    # elif int(sys.argv[1])==2:
        # start = 20000
        # end = 30000

    # elif int(sys.argv[1])==3:
        # start = 30000
        # end = 40000


    # pk = scorpy.PeakData(datapath=patterns_glob[start:end],
                        # geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')




    # im = pk.make_im(1000, 0.127)

    # np.save(f'/media/pat/datadrive/ice/sim/patterns/sums/hex-ice-{size}-{geom}-10k-{sys.argv[1]}', im)

    # plt.figure()
    # plt.imshow(im, origin='lower')


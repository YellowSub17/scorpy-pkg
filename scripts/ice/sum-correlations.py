import numpy as np
import scorpy
import os
import sys
import h5py
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




corrab = scorpy.CorrelationVol(nq=100, npsi=180,qmin=1.5,qmax=3.1, cos_sample=False)

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
print(f'\tSumming correlations for {size}')
print(f'\tstd {std_sf1} to {std_sf2}')
print(f'\tSumming {len(chunk_is)} correlations for part {part.capitalize()}')
for i,  (chunk_i, pattern_i) in  enumerate(zip(chunk_is, pattern_is)):
    print(f'\t{i+1}/{len(chunk_is)}', end='\r')
    path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{chunk_i+1}-{pattern_i+1}-qcor.npy'
    corr = scorpy.CorrelationVol(path=path)
    corrab.vol+=corr.vol
print('\n\tDone.')

corrab.save(f'{scorpy.DATADIR}/ice/sim/corr/sums/stds/hex-ice-{size}-qmin15-std{int(std_sf1*100)}-{int(std_sf2*100)}-{part}-qcor.dbin')


















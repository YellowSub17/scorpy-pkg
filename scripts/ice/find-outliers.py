

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import sys

from scipy.stats import mode




size = '1000nm'
geom ='19MPz18'


# fig1, axes1 = plt.subplots(1,2)
# fig2, axes2 = plt.subplots(1,2)

for color, size in zip([(1,0,0,0.99), (0,1,0, 0.99), (0,0,1,0.99), (1,0,1, 0.8)], ['1000nm', '500nm', '250nm', '125nm']):


    corr_means = np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-means.npy')
    corr_sq_means =np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-sq-means.npy')


    xs = np.sqrt(  corr_means**2 - corr_sq_means  )
    xs_log = np.log10(xs)

    xs_log_counts, xs_log_bins = np.histogram(xs_log, bins=1000)
    xs_log_mean = xs_log.mean()
    xs_log_std = xs_log.std()
    xs_log_median = np.median(xs_log)



    xs_log_mode_loc = int(np.where(xs_log_counts==np.max(xs_log_counts))[0][0])
    xs_log_mode = xs_log_bins[xs_log_mode_loc]
    print(xs_log_mode)


    

    xs_thresh_lower = xs_log_mode+xs_log_std*0
    xs_thresh_upper = xs_log_mode+xs_log_std*1.5















    fig1, axes = plt.subplots(1,1, figsize=(8/2.54, 8/2.54), dpi=300)
    axes = [axes]
    axes[0].stairs(xs_log_counts, xs_log_bins, label=size, color=color)
    axes[0].axvline(x=xs_log_mode, ymin=0, ymax=10, color='black', ls='dashed', label='mode')
    # axes[0].axvline(x=xs_thresh_lower, ymin=0, ymax=10, color='black')
    # axes[0].axvline(x=xs_thresh_upper, ymin=0, ymax=10, color='black')
    axes[0].legend()
    axes[0].set_xlabel('Log Varience Correlating Inten.')
    axes[0].set_ylabel('Counts')
    plt.tight_layout()

    plt.savefig(f'/home/pat/Documents/phd/figs/ice/ice-corr-var-{size}.png')


    cond1 = xs_log > xs_thresh_lower
    cond2 = xs_log <= xs_thresh_upper


    xs_thresh = np.where(np.logical_and(cond1, cond2), xs, 0)

    num_in_thresh = np.sum(xs_thresh>0)




    # xs_counts, xs_bins = np.histogram(xs_thresh[xs_thresh>0], bins=500)
    # xs_mean = xs_thresh.mean()
    # xs_std = xs_thresh.std()
    # xs_median = np.median(xs_thresh)

    # axes[1].stairs(np.log10(np.abs(xs_counts)+1), xs_bins, label=size, color=color)
    # # plt.axvline(x=xs__thresh_lim, ymin=0, ymax=10, color=color)
    # axes[1].legend()

    # print(f'{xs_mean}, {xs_std}, {xs_median}')
    print(f'Num in Thresh:', num_in_thresh)



# axes1[0].legend()
# axes2[0].legend()

plt.show()




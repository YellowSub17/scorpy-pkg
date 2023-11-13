import scorpy
import numpy as np
import matplotlib.pyplot as plt
import glob

import scipy as sp

import matplotlib.cm as cm



data_dir = '/home/ec2-user/corr/data'
geom_code = '19MPz040'
pdb_code = '193l'

corr_dir =  f'{data_dir}/qcor/nsums'



nexponents = 8

nframes_x = [ (2**i)*256 for i in range(nexponents) ]


xtal_sizes = [60, 70,80,90,100,125,150,200,500, ]
xtal_sizes = [70,80,90,100,125,150,200,500, ]
xtal_sizes = [80,90,100,125,150,200,500, ]
# xtal_sizes = [80,500 ]


cmap1 = cm.hsv( np.linspace(0.0, 0.8, len(xtal_sizes)))


css_x  =  np.zeros((nexponents, len(xtal_sizes)))


fig1, axes1 = plt.subplots(1,1)

for i, (xtal_size, color) in enumerate(zip(xtal_sizes, cmap1)):


    for exponent in range(nexponents):
        nframes = (2**exponent)*256

        corr_glob = glob.glob(f'{corr_dir}/*{xtal_size}nm*n{nframes}*.dbin')
        corr_glob.sort()

        if len(corr_glob)%2==1:
            corr_glob = corr_glob[:-1]

        css_s = np.load(f'{data_dir}/css/{pdb_code}-{xtal_size}nm-{geom_code}-x1-n{nframes}-css.npy')
        css_mean = np.mean(css_s)
        css_err = np.std(css_s)
        axes1.errorbar(np.log2(nframes), css_mean, yerr=3*css_err, marker='.', color=color, capsize=0.1)

        css_x[exponent, i] = css_mean









for i, (xtal_size, color) in enumerate(zip(xtal_sizes, cmap1)):



    axes1.plot(xi, yi, color=color, linestyle='dashed', label=f'{xtal_size}nm')
    axes1.errorbar(x0_fit, logistic_fn(x0_fit, L_fit, k_fit, x0_fit), color=color, marker='x', xerr=3*perr[-1])












axes1.set_xlabel('# of Frames')
axes1.set_ylabel('Cosine Similarity')
axes1.legend()





plt.show()


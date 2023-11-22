import scorpy
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', size=8)
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


cmap1 = cm.turbo( np.linspace(0.0, 0.8, len(xtal_sizes)))


css_x =  np.zeros((nexponents, len(xtal_sizes)))


fig1, axes1 = plt.subplots(1,1, figsize=(8/2.54, 8/2.54), dpi=300)

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








def logistic_fn(x, L, k, x0):
    ned = L
    donk = 1+np.exp(-k*(x-x0))
    return ned/donk


lower_bounds = (0.99, 0, 0)
upper_bounds = (1,1,25)




x0s = []
x0_errs = []
ks = []

for i, (xtal_size, color) in enumerate(zip(xtal_sizes, cmap1)):

    
    print(css_x[:,:-1])
    # print(i, xtal_size)

    popt, pcov = sp.optimize.curve_fit(logistic_fn, np.log2(nframes_x), css_x[:, i], bounds = (lower_bounds, upper_bounds))
    perr = np.sqrt(np.diag(pcov))
    print(xtal_size, popt, perr)
    L_fit, k_fit, x0_fit = popt[0], popt[1], popt[2]

    x0s.append(x0_fit)
    x0_errs.append(perr[-1])
    ks.append(k_fit)



    xi = np.linspace(1, 36)
    yi = logistic_fn(xi, L_fit, k_fit, x0_fit)

    axes1.plot(xi, yi, color=color, linestyle='dashed', label=f'{xtal_size}nm')
    # axes1.errorbar(x0_fit, logistic_fn(x0_fit, L_fit, k_fit, x0_fit), color=color, marker='x', xerr=3*perr[-1])






axes1.set_xlim([7.5, 15.5])
axes1.set_ylim([0, 1])
axes1.set_xlabel('# of Frames [$\\log_2(x)$]')
axes1.set_ylabel('Cosine Similarity')
axes1.legend()

plt.tight_layout()





plt.show()


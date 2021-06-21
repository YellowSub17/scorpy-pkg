#!/usr/bin/env python3
'''
make-padf.py

Make padf vol objects.
'''

import scorpy
import numpy as np
np.random.seed(0)



assert False, 'Need to fix corr -1 to 1 before runnning make-padf'

# MAKE PADF FROM PEAKS DATA CORRELATION
# runs150 = [112,123,113,125,102,103,104,105]
# runs144 = [118,108,119,109,120,110,121]
# runs = runs150+runs144

# res = 0.05
# rmax = 12

# nr = round(rmax/res)

# for run in runs:
# cor = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_qcor')
# padf = scorpy.PadfVol(nr,int(cor.npsi/2), rmax)
# qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_qcor.dbin'
# padf.fill_from_corr(qcor_path, nl=31, wavelength=1.33e-10)
# padf.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_highres_padf')


#     for seed in range(20):

# cor = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')
# padf = scorpy.PadfVol(nr,int(cor.ntheta/2), rmax)
# qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor.dbin'
# padf.fill_from_corr(qcor_path, nl=11, wavelength=1.33e-10)
# padf.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_padf')

# cor = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')
# padf = scorpy.PadfVol(nr,int(cor.ntheta/2), rmax)
# qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor.dbin'
# padf.fill_from_corr(qcor_path, nl=11, wavelength=1.33e-10)
# padf.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_padf')


# MAKE PADF FROM PEAKS DATA CORRELATION (multi)

runs150 = [112, 123, 113, 125, 102, 103, 104, 105]
runs144 = [118, 108, 119, 109, 120, 110, 121]
runs = runs150 + runs144


ress = [0.05, 0.1, 0.15, 0.2]  # A/bin
rmaxs = [5, 10, 15, 20]  # A
nls = [11, 21, 31]


for i, run in enumerate(runs):
    for j, res in enumerate(ress):
        for k, nl in enumerate(nls):
            for l, rmax in enumerate(rmaxs):

                nr = round(rmax / res)  # A/(A/bin) = BINS

                cor = scorpy.CorrelationVol(
                    path=f'../data/dbins/cosine_sim/{run}/run{run}_qcor')
                padf = scorpy.PadfVol(nr, int(cor.npsi / 2), rmax, nl, 1.33)
                qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_qcor.dbin'
                padf.fill_from_corr(qcor_path)
                padf.save(
                    f'../data/dbins/cosine_sim/{run}/run{run}_res{j+1}_rmax{rmax}_nl{nl}_padf')


# rmax = 5
# res = 0.01
# nl = 20

# nr = round(rmax/res)
# run = 112

# corr = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_qcor')
# padf = scorpy.PadfVol(nr, int(corr.npsi/2), rmax, nl, 1.33)
# qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_qcor.dbin'
# padf.fill_from_corr(qcor_path)

# padf_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_rm{rmax}padf.dbin'

# padf.save(f'../data/dbins/cosine_sim/{run}/run{run}_padf')

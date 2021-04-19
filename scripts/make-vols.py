#!/usr/bin/env python3
'''
make-vols.py

Make various vol objects.
'''

import timeit
import scorpy
import numpy as np
np.random.seed(0)

print()


def make_correlation_from_cif(names, nq, ntheta, qmax=None, dryrun=False, tag='_qcor'):

    for name in names:
        cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')

        if qmax is None:
            qmax = cif.qmax
        cor = scorpy.CorrelationVol(nq, ntheta, qmax)


        print(f'\n\nStarting Correlation of: {name}')
        print(f'\nnq: {cor.nq}, ntheta: {cor.ntheta}, qmax: {qmax}')
        print(f'Correlating vectors.')
        print(f'\n...')
        if not dryrun:
            cor.correlate(cif.scattering)
        print(f'\nDone.')
        cor.save_dbin(f'../data/dbins/{name}{tag}')



def make_blqq_from_correlation(names=['1al1'], nl=65):

    for name in names:
        cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')
        bl = scorpy.BlqqVol(nq=cor.nq, nl=nl, qmax=cor.qmax)

        print(f'\n\nCalculating Blqq of: {name}')
        print(f'\nnq: {cor.nq}, nl: {nl}, qmax: {cor.qmax}')

        print(f'\n...')
        bl.fill_from_corr(cor)
        print(f'\nDone.')


        bl.save_dbin(f'../data/dbins/{name}_blqq')




def make_corr_from_peakdata():
## PeakData

    runs150 = [112,123,113,125,102,103,104,105]
    runs144 = [118,108,119,109,120,110,121]
    runs = runs150+runs144

    geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

    for run in runs:
        print(f'Run: {run}')
        peaks = scorpy.PeakData(f'../data/cxi/{run}/peaks.txt', geo)

        cor = scorpy.CorrelationVol(100,180, 1.4)

        for frame in peaks.split_frames():
            if frame.qlist.shape[0] < 150:
                cor.correlate(frame.qlist[:,-3:])
        cor.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_qcor')



def make_corr_from_peakdata_half():
## PeakData (Half runs)
    runs150 = [112,123,113,125,102,103,104,105]
    runs144 = [118,108,119,109,120,110,121]
    runs = runs150+runs144

    geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

    for run in runs:

        print(f'Run: {run}')
        peaks = scorpy.PeakData(f'../data/cxi/{run}/peaks.txt', geo)
        frames = [i for i in peaks.split_frames() if i.qlist.shape[0]<150]
        half_ind = int(len(frames)/2)


        for seed in range(20):
            print(f'Seed: {seed}')

            correl_frames = list(frames)
            np.random.shuffle(correl_frames)

            cora_frames = correl_frames[:half_ind]
            corb_frames = correl_frames[half_ind:]

            cora = scorpy.CorrelationVol(100,180, 1.4)
            for frame in cora_frames:
                cora.correlate(frame.qlist[:,-3:])
            cora.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')

            corb = scorpy.CorrelationVol(100,180, 1.4)
            for frame in corb_frames:
                corb.correlate(frame.qlist[:,-3:])
            corb.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')


### PadfVol

def make_padf_from_correlation():

    runs150 = [112,123,113,125,102,103,104,105]
    runs144 = [118,108,119,109,120,110,121]
    runs = runs150+runs144

    res = 0.25
    rmax = 30
   

    nr = round(rmax/res)


    for run in runs:
        cor = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_qcor')
        padf = scorpy.PadfVol(nr,cor.ntheta, rmax)

        qcor_path = f'/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/dbins/cosine_sim/{run}/run{run}_qcor.dbin'
        padf.fill_from_corr(qcor_path, nl=11)

        padf.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_padf')

# run_padf(cor, 30,0.25, 10, f'{outpath}', tag=f'seed{seed}_a')

# def run_padf(cor,rmax, res, nl, outpath, tag='tag'):

if __name__ =="__main__":


    print('Make Vols')

    # make_correlation_from_cif(names=['1al1'], nq=200, ntheta=400, qmax=0.18, dryrun=False, tag='x')
    # make_blqq_from_correlation()
    make_padf_from_correlation()
    # make_corr_from_peakdata_half()
    # make_corr_from_peakdata()
















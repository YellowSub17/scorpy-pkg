#!/usr/bin/env python3
'''
make-corr.py

Make correlation vol objects.
'''

import scorpy
import numpy as np
np.random.seed(0)




# #### MAKE CORRELATION FROM CIF DATA
# names  =['1al1'] # 1al1 qmax 0.36992983463258367
# nq = 100
# ntheta = 180

# qmax = 0.36992983/2



# for name in names:
    # print(f'Correlating: {name}')
    # cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=qmax)
    # cor = scorpy.CorrelationVol(nq, ntheta, qmax=cif.qmax)
    # cor.correlateSPH(cif.spherical)
    # cor.save_dbin(f'../data/dbins/{name}_sph_qcor')


    # cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=qmax)
    # cif.bin_spherical(nq, ntheta, ntheta)
    # cor = scorpy.CorrelationVol(nq, ntheta, qmax=cif.qmax)
    # cor.correlateSPH(cif.spherical)
    # cor.save_dbin(f'../data/dbins/{name}_binned_sph_qcor')

    # cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=qmax)
    # cif.bin_spherical(int(nq/2), int(ntheta/2), int(ntheta/2))
    # cor = scorpy.CorrelationVol(nq, ntheta, qmax=cif.qmax)
    # cor.correlateSPH(cif.spherical)
    # cor.save_dbin(f'../data/dbins/{name}_binned_half_sph_qcor')

    # cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif', qmax=qmax)
    # cif.bin_spherical(2*nq, 2*ntheta, 2*ntheta )
    # cor = scorpy.CorrelationVol(nq, ntheta, qmax=cif.qmax)
    # cor.correlateSPH(cif.spherical)
    # cor.save_dbin(f'../data/dbins/{name}_binned_double_sph_qcor')







#### MAKE CORRELATION FROM PEAK DATA

runs150 = [112,123,113,125,102,103,104,105]
runs144 = [118,108,119,109,120,110,121]
runs = runs150+runs144



nseeds = 20
nq = 200
ntheta = 360
qmax = 1.4
npeaksmax = 150

geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

for run in runs:

    print(f'Correlating run: {run}')
    peaks = scorpy.PeakData(f'../data/cxi/{run}/peaks.txt', geo)
    frames = [i for i in peaks.split_frames() if i.scat_pol.shape[0]<npeaksmax]
    half_ind = int(len(frames)/2)



    corr = scorpy.CorrelationVol(nq,ntheta, qmax)
    for frame in frames:
        corr.fill_from_peakdata(frame)
    corr.save(f'../data/dbins/cosine_sim/{run}/run{run}_qcor')


#     for seed in range(nseeds):
        # print(f'Correlating seed: {seed}')

        # seed_frames = list(frames)
        # np.random.shuffle(seed_frames)

        # corra_frames = seed_frames[:half_ind]
        # corrb_frames = seed_frames[half_ind:]

        # corra = scorpy.CorrelationVol(nq,ntheta,qmax)
        # for frame in corra_frames:
            # corra.fill_from_peakdata(frame)
        # corra.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')

        # corrb = scorpy.CorrelationVol(nq,ntheta,qmax)
        # for frame in corrb_frames:
            # corrb.fill_from_peakdata(frame)
        # corrb.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')



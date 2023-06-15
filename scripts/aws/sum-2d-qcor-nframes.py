

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import subprocess
import h5py
import scipy as sp
import time




data_dir = '/home/ec2-user/corr/data'

xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'

#some power of 2
# nframes = sys.argv[1]


#exponent of two between 0 and 6 inclus.
exp = int(sys.argv[1])

nchunks = 2**exp
chunk_start = nchunks -1
chunk_end = chunk_start + nchunks

nframes = 256*nchunks


print(f'Summing frames for a and b sets.')
print(f'Using {nchunks} chunks from {chunk_start} to {chunk_end}.')
print(f'Total frames in a and b sets: {nframes} frames.')








# # #frames 0 to 255 are for the correlations A set
# # #frames 256 to 511 are for the correlations B set

# # #chunk 0 for n256
# # #chunk 1 to 2 for n512
# # #chunk 3 to 6 for n1024
# # #chunk 7 to 14 for n2048
# # #chunk 15 to 30 for n4096


corra = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
corrb = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
for i_chunk in range(chunk_start, chunk_end):
    print(f'Summing chunk: {i_chunk}')
    # print(f'Started: {time.asctime()}')

    corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}/{i_chunk}'

    for i_frame in range(256):
        print(i_frame, end='\r')
        qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{i_chunk}-{i_frame}-qcor.npy'
        frame_corr = scorpy.CorrelationVol(path=qcor_path)
        corra.vol += frame_corr.vol

    for i_frame in range(256, 512):
        print(i_frame, end='\r')
        qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{i_chunk}-{i_frame}-qcor.npy'
        frame_corr = scorpy.CorrelationVol(path=qcor_path)
        corrb.vol += frame_corr.vol


corra.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-n{nframes}-a-qcor.dbin')
corrb.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-n{nframes}-b-qcor.dbin')

    # print(f'Finished: {time.asctime()}')





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
geom_code = '19MPz040'
pdb_code = '193l'




xtal_size = sys.argv[1]
super_chunk = sys.argv[2]


exp_start = int(sys.argv[3])
reverse_flag = bool(int(sys.argv[4]))


if reverse_flag:
    exps = [i for i in range(exp_start, -1, -1)]
    chunks = [i for i in range(255, -1, -1)]
    set_names='stuvwxyz'
else:
    exps = [i for i in range(exp_start, -1, -1)]
    chunks = [i for i in range(0, 256)]
    set_names='abcdefgh'

set_name = set_names[exp_start]










chunk_start = 0

for exp in exps:
    
    nchunks =2**exp
    nframes = nchunks*256

    chunk_end = chunk_start+nchunks



    print(xtal_size, super_chunk, nframes, set_name, chunk_start, chunk_end)
    corra = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
    corrb = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

    for i_chunk in chunks:
        print(f'Summing chunk: {i_chunk}')

        corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}/{i_chunk}'

        for i_frame in range(256):
            print(i_frame, end='\r')
            qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{i_chunk}-{i_frame}-qcor.npy'
            frame_corr = scorpy.CorrelationVol(path=qcor_path)
            corra.vol += frame_corr.vol

        for i_frame in range(256, 512):
            print(i_frame, end='\r')
            qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{i_chunk}-{i_frame}-qcor.npy'
            frame_corr = scorpy.CorrelationVol(path=qcor_path)
            corrb.vol += frame_corr.vol


    chunk_start = chunk_end


    corra.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-n{nframes}-{set_name}1-qcor.dbin')
    corrb.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-n{nframes}-{set_name}2-qcor.dbin')




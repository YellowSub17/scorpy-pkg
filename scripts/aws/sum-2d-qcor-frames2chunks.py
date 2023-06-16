

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


chunk_start = int(sys.argv[1])
chunk_end = int(sys.argv[2])

print(f'Summing chunks: {chunk_start}-{chunk_end}')


for i_chunk in range(chunk_start, chunk_end):
    print(f'Summing chunk: {i_chunk}')
    print(f'Started: {time.asctime()}')

    chunk_corr = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

    corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}/{i_chunk}'

    for i_frame in range(500):


        qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{i_chunk}-{i_frame}-qcor.npy'

        frame_corr = scorpy.CorrelationVol(path=qcor_path)

        chunk_corr.vol +=frame_corr.vol

    chunk_corr.save(f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{i_chunk}-chunksum-qcor.npy')


    print(f'Finished: {time.asctime()}')














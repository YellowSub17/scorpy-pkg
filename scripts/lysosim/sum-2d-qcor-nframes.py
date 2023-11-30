

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
my_exponent = int(sys.argv[3])
max_exponent = int(sys.argv[4])
reverse_flag = bool(int(sys.argv[5]))






exponents = [i for i in range(max_exponent, -1, -1)]
if not reverse_flag:
    chunks = [i for i in range(0, 256)]
    set_names ='abcdefgh'
else:
    chunks = [i for i in range(255, -1, -1)]
    set_names ='zyxwvuts'
set_name = set_names[max_exponent]





#### generate chunk ranges
# print(f'{exponents=}')


chunk_end_index = 0
for exponent in exponents:
    chunk_start_index = chunk_end_index
    nchunks = 2**exponent
    nframes = nchunks*256
    chunk_end_index = chunk_start_index + nchunks

    if exponent==my_exponent:
        break

# if reverse_flag:
    # tmp_var = chunk_start_index
    # chunk_start_index = chunk_end_index
    # chunk_end_index = tmp_var





chunk_start = chunks[chunk_start_index]
chunk_end = chunks[chunk_end_index]




print(f'Summing Correlations: {xtal_size}, {nframes} frames, Set {set_name}')
print(f'Chunk range: {chunk_start} to {chunk_end} ({nchunks} total)')
# corr1 = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
# corr2 = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

corr1 = scorpy.CorrelationVol(nq=200, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)
corr2 = scorpy.CorrelationVol(nq=200, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)

print(20*'. ')

# print(f'{chunk_start_index=} {chunk_end_index=}')
# print(chunks[chunk_start_index:chunk_end_index])

for i_chunk, chunk in enumerate(chunks[chunk_start_index:chunk_end_index]):
    print(f'{i_chunk}\t/{nchunks}', end='\r')


    corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}/{chunk}'

    for i_frame in range(256):
        qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{i_frame}-qcor.npy'
        frame_corr = scorpy.CorrelationVol(path=qcor_path)
        corr1.vol += frame_corr.vol

    for i_frame in range(256, 512):
        qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{i_frame}-qcor.npy'
        frame_corr = scorpy.CorrelationVol(path=qcor_path)
        corr2.vol += frame_corr.vol

print(20*'. ')


corr1.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-n{nframes}-{set_name}1-qcor.dbin')
corr2.save(f'{data_dir}/qcor/nsums/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-n{nframes}-{set_name}2-qcor.dbin')
print('Done.')




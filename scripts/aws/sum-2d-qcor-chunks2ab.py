

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



print(f'Summing chunks into ab sets.')

corr_a = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
corr_b = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

for i_chunk in range(80):
    print(f'Chunk:\t{i_chunk}',end='\r')

    corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}/{i_chunk}'
    chunk_corr = scorpy.CorrelationVol(path=f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{i_chunk}-chunksum-qcor.npy')



    if i_chunk %2 ==0:
        corr_a.vol += chunk_corr.vol
    else:
        corr_b.vol += chunk_corr.vol



corr_ab_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}'
corr_a.save(f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-a-qcor.dbin')
corr_b.save(f'{corr_ab_dir}/{pdb_code}-{xtal_size}-{geom_code}-b-qcor.dbin')

print('')
print('Done.')

















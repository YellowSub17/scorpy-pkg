

import scorpy
import numpy as np

import matplotlib.pyplot as plt

import os
import sys
import subprocess
import h5py
import scipy as sp
import time


#options
pdb_code = sys.argv[1]
geom_code = sys.argv[2]
chunk = sys.argv[3]
n_patterns = int(sys.argv[4])
xtal_size = int(sys.argv[5])


#filenames
geom_file = f'/home/ec2-user/corr/data/geom/{geom_code}.geom'
hkl_file =  f'/home/ec2-user/corr/data/xtal/{pdb_code}.hkl'
pdb_file =  f'/home/ec2-user/corr/data/xtal/{pdb_code}.pdb'
out_file =  f'/home/ec2-user/corr/data/frames/{pdb_code}-{xtal_size}nm-{geom_code}-{chunk}'


#patternsim commands
cmd = []
cmd.append('pattern_sim')
cmd.append('--gpu')
cmd.append(f'--number={n_patterns}')
cmd.append(f'--max-size={xtal_size}')
cmd.append(f'--min-size={xtal_size}')
cmd.append(f'--nphotons=1e12')
cmd.append(f'--spectrum=tophat')
cmd.append(f'--sample-spectrum=1')
cmd.append('--random-orientation')
cmd.append('--really-random')

cmd.append(f'--geometry={geom_file}')
cmd.append(f'--intensities={hkl_file}')

cmd.append(f'--pdb={pdb_file}')
cmd.append(f'--output={out_file}')


print(f'Generating {n_patterns} patterns of protein {pdb_code} using geometry {geom_code}')

print(f'Starting at: {time.asctime()}')
subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print(f'Finished at: {time.asctime()}')




print('Resaving h5s to npz')
print(f'Starting at: {time.asctime()}')
for i_pattern in range(1, n_patterns+1):

    h5_fname = f"{out_file}-{i_pattern}.h5"
    npz_fname = f"{out_file}-{i_pattern-1}.npz"

    with h5py.File(h5_fname) as h5file:

        d = h5file['/entry_1/instrument_1/detector_1/data'][:]
        coo = sp.sparse.coo_matrix(d)
        sp.sparse.save_npz(npz_fname, coo)

    cmd = []
    cmd.append('rm')
    cmd.append(h5_fname)
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print(f'Finished at: {time.asctime()}')


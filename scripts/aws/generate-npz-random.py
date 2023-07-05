

import scorpy
import numpy as np

import matplotlib.pyplot as plt

import os
import sys
import subprocess
import h5py
import scipy as sp
import time
import scipy.spatial.transform as scit



if len(sys.argv)<3:
    print('''
    pdb_code = "193l"
    geom_code = "19MPz040"
    super_chunk = sys.argv[1]
    chunk = sys.argv[2]
    xtal_size = int(sys.argv[3])
    n_patterns = 512 # if not sys.argv[4]
    ''')

#options
pdb_code = "193l"
geom_code = "19MPz040"
super_chunk = sys.argv[1]
chunk = sys.argv[2]
xtal_size = int(sys.argv[3])

if len(sys.argv)>3:
    n_patterns = int(sys.argv[4])
else:
    n_patterns = 512


#filenames
geom_file = f'/home/ec2-user/corr/data/geom/{geom_code}.geom'
hkl_file =  f'/home/ec2-user/corr/data/xtal/{pdb_code}.hkl'
pdb_file =  f'/home/ec2-user/corr/data/xtal/{pdb_code}.pdb'
out_path =  f'/home/ec2-user/corr/data/frames/{xtal_size}nm-{geom_code}-{super_chunk}/{chunk}'
out_fname =  f'{pdb_code}-{xtal_size}nm-{geom_code}-{super_chunk}-{chunk}'
out_file = f'{out_path}/{out_fname}'


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
cmd.append('--no-fringes')
cmd.append(f'--geometry={geom_file}')
cmd.append(f'--intensities={hkl_file}')
cmd.append(f'--pdb={pdb_file}')
cmd.append(f'--output={out_file}')


# out_fname =  f'{pdb_code}-{xtal_size}nm-{geom_code}-{super_chunk}-{chunk}'
print('####')
print(f'Generating {out_fname}-[0-{n_patterns}]')
print(f'Starting at: {time.asctime()}')

print('Making npz', end='\r')
p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)





print('Making h5s', end='\r')
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
print()


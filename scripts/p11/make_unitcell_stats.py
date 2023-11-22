

import os
import sys
import numpy as np
import scorpy
import regex as re



def grep(s, reg, fn=None):
    # print(f'greping reg: {reg}')
    found = re.findall(reg, s)
    if fn is not None:
        found = list(map(fn, found))
    return found

datapath = f'/home/ec2-user/corr/data/p11'


runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# runs = [i for i in range( 11, 25 )] 
# runs = [i for i in range(40, 61) ]

# runs = [ 18] 

for run in runs:
    print(f'Starting run:\t{run}')
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'

    crystfeltotal_file = open(f'{runpath}/crystfel.total.edit', 'r')

    cont = crystfeltotal_file.read()



    found_str = re.findall( r'(?<=Cell parameters .*)(\d+.\d+)', cont  )

    found_flt = list(map(float, found_str))

    unitcells = np.array(found_flt).reshape(int(len(found_flt)/6), 6)

    np.save(f'{runpath}/unitcells.npy', unitcells)
    

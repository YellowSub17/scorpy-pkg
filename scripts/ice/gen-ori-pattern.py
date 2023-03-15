


import scorpy
import os

import sys
import subprocess


#PARAMETERS


xtal_size = 100
geom = '19MPz18'

cmd = []
cmd.append('/home/pat/Downloads/crystfel-0.10.2/build/pattern_sim')
cmd.append('--gpu')


cmd.append(f'--number={3}')
cmd.append(f'--max-size={xtal_size}')
cmd.append(f'--min-size={xtal_size}')
cmd.append(f'--nphotons={1e12}')
cmd.append(f'--spectrum=tophat')
cmd.append(f'--sample-spectrum=1')

# cmd.append('--random-orientation')
# cmd.append('--really-random')

# cmd.append(f'--template={scorpy.DATADIR}/ice/sim/struct/ori.stream')


cmd.append(f'--geometry={scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')
cmd.append(f'--intensities={scorpy.DATADIR}/ice/sim/struct/hex-ice-p1-d05.hkl')

cmd.append(f'--pdb={scorpy.DATADIR}/ice/sim/struct/hex-ice.pdb')
cmd.append(f'--output={scorpy.DATADIR}/ice/sim/patterns/hex-ice-xy')

# print(f'Creating {n_patterns} patterns.')

print(*cmd, sep=' ')

## cat ori.stream | cmd

# subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



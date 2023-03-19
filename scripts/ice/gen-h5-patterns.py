


import scorpy
import os

import sys
import subprocess


#PARAMETERS


chunk = sys.argv[1]
n_patterns = sys.argv[2]
xtal_size = sys.argv[3]
geom = sys.argv[4]

cmd = []
cmd.append('/home/pat/Downloads/crystfel-0.10.2/build/pattern_sim')
cmd.append('--gpu')
cmd.append(f'--number={n_patterns}')

cmd.append(f'--max-size={xtal_size}')
cmd.append(f'--min-size={xtal_size}')
cmd.append(f'--nphotons={1e12}')
# cmd.append(f'--no-fringes')
cmd.append(f'--spectrum=tophat')
cmd.append(f'--sample-spectrum=1')

cmd.append('--random-orientation')
cmd.append('--really-random')


cmd.append(f'--geometry={scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')
cmd.append(f'--intensities={scorpy.DATADIR}/ice/sim/struct/hex-ice-p1-d05.hkl')

cmd.append(f'--pdb={scorpy.DATADIR}/ice/sim/struct/hex-ice.pdb')
cmd.append(f'--output={scorpy.DATADIR}/ice/sim/patterns/{geom}/{xtal_size}nm/hex-ice-{xtal_size}nm-{geom}-{chunk}')

# print(f'Creating {n_patterns} patterns.')

# print(*cmd, sep=' ')


subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



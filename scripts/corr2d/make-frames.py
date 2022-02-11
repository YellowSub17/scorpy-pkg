

import scorpy

import os


gpu = True
randomor = True
rrandom = True
nofringe = True
nonoise = True
flat = True
ncrystrals = 10
background = 0
maxsize = 10
minsize = 10
beamr = 1e-6
nphotons = 1e12
beamband = 0.001
photonenergy = 9300
spectrum= 'tophat'
specsample = 1
gradient = 'mosaic'
geom = f'{scorpy.DATADIR}/geoms/agipd_2304_vj_opt_v3.geom'
pdb = f'{scorpy.DATADIR}/pdb/1vds.pdb'
outpath = f'{scorpy.DATADIR}/patternsim/test'




cmd = 'pattern_sim '

if gpu:
    cmd+='--gpu '
if randomor:
    cmd+='--random-orientation '
if rrandom:
    cmd+='--really-random '
if nofringe:
    cmd+='--no-fringes '
if nonoise:
    cmd+='--no-noise '
if flat:
    cmd+='--flat '

cmd+=f'--n {ncrystrals} '
cmd+=f'--background={background} '

cmd+=f'--max-size={maxsize} '
cmd+=f'--min-size={minsize} '
cmd+=f'--beam-radius={beamr} '
cmd+=f'--nphotons={nphotons} '
cmd+=f'--beam-bandwidth={beamband} '
cmd+=f'--photon-energy={photonenergy} '

cmd+=f'--spectrum={spectrum} '
cmd+=f'--sample-spectrum={specsample} '
cmd+=f'--gradients={gradient} '
cmd+=f'-g {geom} '
cmd+=f'-p {pdb} '
cmd+=f'-o {outpath} '

print(cmd)



####py make-frames.py | bash 


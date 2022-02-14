

import scorpy

import os


## parameters
gpu = True
randomor = True
nofringe = True
nonoise = True
flat = True
ncrystals = 1000
background = 0
maxsize = 1000
minsize = 1000

# maxsize = 100
# minsize = 100
beamr = 1e-12
nphotons = 1e12
beamband = 0.001
photonenergy = 9000
spectrum= 'tophat'
specsample = 1
gradient = 'mosaic'
geom = f'{scorpy.DATADIR}/geoms/single_square.geom'
pdb = f'{scorpy.DATADIR}/pdb/1vds.pdb'
outpath = f'{scorpy.DATADIR}/patternsim/plot-test'
outpath = f'{scorpy.DATADIR}/patternsim/1vds/1vds'




if ncrystals>1 and outpath[-3:]=='.h5':
    outpath = outpath[:-3]
elif ncrystals==1 and outpath[-3:] != '.h5':
    outpath += '.h5'


cmd = 'pattern_sim '

if randomor:
    cmd+='--random-orientation '
    cmd+='--really-random '

if gpu:
    cmd+='--gpu '
if nofringe:
    cmd+='--no-fringes '
if nonoise:
    cmd+='--no-noise '
if flat:
    cmd+='--flat '

cmd+=f'-n {ncrystals} '
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


# ori = '0.685 0.591 0.098 0.414'
# print(ori)
# ori = '0.717 0.514 -0.039 0.470'
# print(ori)

# if not randomor:
    # print(ori)

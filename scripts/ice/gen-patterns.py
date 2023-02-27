


import scorpy
import os



#PARAMETERS

xtal_size = 1e3
n_patterns = 10000
n_photons = 1e12




cmd = '~/Downloads/crystfel-0.10.2/build/pattern_sim '
cmd+='--gpu '
cmd+=f'--number {n_patterns} '

cmd+=f'--max-size={xtal_size} '
cmd+=f'--min-size={xtal_size} '
cmd+=f'--nphotons={n_photons} '
# cmd+=f'--no-fringes '
cmd+=f'--spectrum=tophat '
cmd+=f'--sample-spectrum=1 '

cmd+='--random-orientation '
cmd+='--really-random '


cmd+=f'-g {scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom '
cmd+=f'--intensities={scorpy.DATADIR}/ice/sim/struct/hex-ice-p1.hkl '

cmd+=f'--pdb={scorpy.DATADIR}/ice/sim/struct/hex-ice.pdb '
cmd+=f'--output={scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um '

os.system(f'{cmd}')




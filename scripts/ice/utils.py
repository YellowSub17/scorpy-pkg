


import scorpy
import os








def gen_pattern(size, nphotons=1e22, photonenergy=9300, pdb='hex-ice'):
    print("# Generating Pattern")

    cmd = 'pattern_sim '
    # cmd+='--gpu '
    # cmd+=f'--number 2 '
    cmd+=f'--max-size={size} '
    cmd+=f'--min-size={size} '
    cmd+=f'--nphotons={nphotons} '
    cmd+=f'--photon-energy={photonenergy} '
    # cmd+=f'--no-fringes '
    cmd+=f'--spectrum=tophat '
    cmd+=f'--sample-spectrum=1 '
    cmd+=f'--gradients=mosaic '

    cmd+='--random-orientation '
    cmd+='--really-random '

    

    cmd+=f'-g {scorpy.DATADIR}/ice/sim/geoms/detector.geom '
    cmd+=f'--intensities={scorpy.DATADIR}/ice/sim/struct/{pdb}.hkl '
    cmd+=f'--pdb={scorpy.DATADIR}/ice/sim/struct/{pdb}.pdb '
    cmd+=f'--output={scorpy.DATADIR}/ice/sim/patterns/x.h5 '

    os.system(f'{cmd}')



if __name__=='__main__':
    print('Running Utils')

    gen_pattern()



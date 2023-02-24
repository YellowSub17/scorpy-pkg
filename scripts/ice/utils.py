


import scorpy
import os








def gen_pattern(size=1e3, nph=1e12, ev=9300, random=True):
    print("# Generating Pattern")

    cmd = 'pattern_sim '
    # cmd+='--gpu '
    # cmd+=f'--number 2 '
    cmd+=f'--max-size={size} '
    cmd+=f'--min-size={size} '
    cmd+=f'--nphotons={nph} '
    cmd+=f'--photon-energy={ev} '
    # cmd+=f'--no-fringes '
    cmd+=f'--spectrum=tophat '
    cmd+=f'--sample-spectrum=1 '
    cmd+=f'--gradients=mosaic '

    if random:
        cmd+='--random-orientation '
        cmd+='--really-random '


    cmd+=f'-g {scorpy.DATADIR}/ice/sim/geoms/detector.geom '
    cmd+=f'--intensities={scorpy.DATADIR}/ice/sim/struct/hex-ice-p1.hkl '

    cmd+=f'--pdb={scorpy.DATADIR}/ice/sim/struct/hex-ice.pdb '
    cmd+=f'--output={scorpy.DATADIR}/ice/sim/patterns/x.h5 '

    os.system(f'{cmd}')



if __name__=='__main__':

    gen_pattern()






import scorpy
import os




def write_geom(clen=0.18, photonenergy=9300, pixsize=2e-4, npix=1024):
    print('#Writing geometry file')
    geomf  = open(f'{scorpy.DATADIR}/ice/sim/detector.geom', 'w')

    geomf.write(f'data = /entry_1/instrument_1/detector_1/data\n')
    geomf.write(f'mask = /entry_1/instrument_1/detector_1/mask\n')
    geomf.write(f'adu_per_eV = 0.0075\n')
    geomf.write(f'clen = {clen}\n')
    geomf.write(f'photon_energy = {photonenergy}\n')
    geomf.write(f'dim0 = %\n')
    geomf.write(f'dim1 = ss\n')
    geomf.write(f'dim2 = fs\n')
    geomf.write(f'res = {int(1/pixsize)}\n')
    geomf.write(f'p0/min_fs = 0\n')
    geomf.write(f'p0/min_ss = 0\n')
    geomf.write(f'p0/max_fs = {npix}\n')
    geomf.write(f'p0/max_ss = {npix}\n')
    geomf.write(f'p0/corner_x = -{int(npix/2)}\n')
    geomf.write(f'p0/corner_y = -{int(npix/2)}\n')
    geomf.write(f'p0/coffset = 0\n')
    geomf.write(f'p0/fs = +0.0x +1.0y\n')
    geomf.write(f'p0/ss = +1.0x +0.0y\n')
    geomf.close()



def gen_pattern(size=90, nphotons=1e12, photonenergy=9300, pdb='hex-ice'):
    print("# Generating Pattern")

    cmd = 'pattern_sim '
    # cmd+='--gpu '
    cmd+=f'-n 1 '
    cmd+=f'--max-size={size} '
    cmd+=f'--min-size={size} '
    cmd+=f'--nphotons={nphotons} '
    cmd+=f'--photon-energy={photonenergy} '
    cmd+=f'--no-fringes '
    cmd+=f'--spectrum=tophat '
    cmd+=f'--sample-spectrum=1 '
    cmd+=f'--gradients=mosaic '

    cmd+='--random-orientation '
    cmd+='--really-random '

    cmd+=f'-g {scorpy.DATADIR}/ice/sim/detector.geom '
    cmd+=f'--intensities={scorpy.DATADIR}/ice/sim/{pdb}.hkl '
    cmd+=f'--pdb={scorpy.DATADIR}/ice/sim/{pdb}.pdb '
    cmd+=f'--output={scorpy.DATADIR}/ice/sim/test-pattern.h5 '

    os.system(f'{cmd}')






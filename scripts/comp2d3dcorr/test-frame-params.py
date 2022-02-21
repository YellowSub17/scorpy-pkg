

import scorpy

import os
import sys
import matplotlib.pyplot as plt


## parameters
size = 1000
photonenergy = 9300
qmax=1
qmin=0.01
clen = 0.19
npix = 1000
pixsize = 800e-6

geompath = f'{scorpy.DATADIR}/geoms/single_square.geom'
pdbpath = f'{scorpy.DATADIR}/pdb/dummy.pdb'
intenpath = f'{scorpy.DATADIR}/cifs/1vds-qmax1-sf.hkl'





geomfname = 'plot-test.geom'
geomf = open(f'{geompath}', 'w')
geomf.write('data = /entry_1/instrument_1/detector_1/data\n')
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
geomf.write(f'nfs = {npix}\n')
geomf.write(f'nss = {npix}\n')
geomf.close()




cmd = 'pattern_sim '
cmd+='--random-orientation '
cmd+='--really-random '
cmd+='--gpu '
cmd+=f'-n 1 '
cmd+=f'--max-size={size} '
cmd+=f'--min-size={size} '
cmd+=f'--nphotons=1e12 '
cmd+=f'--photon-energy={photonenergy} '
cmd+=f'--intensities={intenpath} '



cmd+=f'--spectrum=tophat '
cmd+=f'--sample-spectrum=1 '
cmd+=f'--gradients=mosaic '
cmd+=f'-g {geompath} '
cmd+=f'-p {pdbpath} '
cmd+=f'-o {scorpy.DATADIR}/patternsim/plot-test.h5'



# os.system(f'echo "-0.335 -0.004 -0.091 0.938" | {cmd}')
os.system(f'{cmd}')


geo = scorpy.ExpGeom(f'{geompath}')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo)
print(pk.scat_pol.shape[0])

im = pk.make_im(npix=npix, r=npix*pixsize/2, bool_inten=True )

plt.figure()
plt.imshow(im)


pk.plot_peaks()
pk.geo.plot_qring(qmax)
pk.geo.plot_qring(qmin)


plt.show()

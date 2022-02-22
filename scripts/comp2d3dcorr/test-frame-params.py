

import scorpy

import os
import sys
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np


## parameters

size = 75
photonenergy = 9300
qmax=1
qmin=0.01
clen = 0.45
npix = 250
pixsize = 800e-6
nphotons=1e24
nofringes=True

geompath = f'{scorpy.DATADIR}/geoms/plot-test.geom'
pdbpath = f'{scorpy.DATADIR}/xtal/inten1-qmax1.pdb'
intenpath = f'{scorpy.DATADIR}/xtal/inten1-qmax1-sf.hkl'





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
cmd+=f'--nphotons={nphotons} '
cmd+=f'--photon-energy={photonenergy} '
cmd+=f'--intensities={intenpath} '
if nofringes:
    cmd+=f'--no-fringes '
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



# im = pk.make_im(npix=npix, r=npix*pixsize/2, bool_inten=False )

# plt.figure()
# plt.imshow(im)


pk.plot_peaks(scatter=True, cmap='spring')
ax = plt.gca()
ax.set_facecolor("black")
pk.geo.plot_qring(qmax)
pk.geo.plot_qring(qmin)


for q in [0.095, 0.125, 0.155, 0.185, 0.205]:
    pk.geo.plot_qring(q, ec='red')

print('npeaks:', pk.scat_rect.shape[0])



# loc = np.where(pk.scat_rect[:,-1] < 0.125* pk.scat_rect[:,-1].max())
# pk.scat_rect[loc] *= 0
# pk.plot_peaks(scatter=True, cmap='spring')
# ax = plt.gca()
# ax.set_facecolor("black")
# pk.geo.plot_qring(qmax)
# pk.geo.plot_qring(qmin)
# for q in [0.095, 0.125, 0.155, 0.185, 0.205]:
    # pk.geo.plot_qring(q, ec='red')




plt.show()

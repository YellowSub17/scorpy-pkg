

import scorpy

import os
import sys
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np


## parameters

size = 75
photonenergy = 9300
qmax=0.264
qmin=0.01
clen = 0.45
npix = 250
pixsize = 800e-6
nphotons=1e24
nofringes=True
integration_r = 0.005
pdbfname = 'inten1-qmax1.pdb'
intenfname = 'inten1-qmax1-sf.hkl'

geomfname = 'plot-test.geom'






geompath = f'{scorpy.DATADIR}/geoms/{geomfname}'



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
cmd+='--gpu '
cmd+=f'-n 1 '
cmd+=f'--max-size={size} '
cmd+=f'--min-size={size} '
cmd+=f'--nphotons={nphotons} '
cmd+=f'--photon-energy={photonenergy} '
cmd+=f'--intensities={scorpy.DATADIR}/xtal/{intenfname} '
if nofringes:
    cmd+=f'--no-fringes '
cmd+=f'--spectrum=tophat '
cmd+=f'--sample-spectrum=1 '
cmd+=f'--gradients=mosaic '
cmd+=f'-g {scorpy.DATADIR}/geoms/{geomfname} '
cmd+=f'-p {scorpy.DATADIR}/xtal/{pdbfname} '
cmd+=f'-o {scorpy.DATADIR}/patternsim/plot-test.h5 '





# os.system(f'echo "0.803 -0.469 0.343 -0.131" | {cmd}')

cmd+='--random-orientation '
cmd+='--really-random '
os.system(f'{cmd}')


geo = scorpy.ExpGeom(f'{geompath}')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo)#, qmax=qmax, qmin=qmin)

pk.plot_peaks(cmap='spring')
ax = plt.gca()
ax.set_facecolor("black")
pk.geo.plot_qring(qmax)
pk.geo.plot_qring(qmin)


# # for q in [0.095, 0.125, 0.155, 0.185, 0.205]:
# for q in [0.089, 0.1275, 0.1555, 0.17975, 0.21]:
    # pk.geo.plot_qring(q, ec='red')



print(pk.scat_rect)
pk_int = pk.integrate_peaks(integration_r)
print(pk_int.scat_rect)

pk_int.plot_peaks(cmap='spring')
ax = plt.gca()
ax.set_facecolor("black")
pk.geo.plot_qring(qmax)
pk.geo.plot_qring(qmin)
pk_int.geo.plot_qring(scorpy.utils.convert_r2q(integration_r, pk.geo.clen, pk.geo.wavelength), ec='green')




plt.show()

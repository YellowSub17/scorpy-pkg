

import scorpy

import os
import sys
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np


## parameters

size = 1450
photonenergy = 9300
qmax=1
clen =0.901
npix = 2000
pixsize = 200e-6

# npix = 100
# pixsize = 0.002

# npix = 250
# pixsize = 800e-6

nphotons=1e24
nofringes=True
integration_r = 0.005
pdbfname = 'p1-intenr.pdb'
intenfname = 'p1-intenr-sf.hkl'

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

# os.system(f'echo "1.000 0.000 0.000 0.000" | {cmd}')
# os.system(f'echo "0.000 0.000 1.000 0.000" | {cmd}')

# os.system(f'echo "0.854 0.146 0.354 0.354" | {cmd}')

cmd+='--random-orientation '
cmd+='--really-random '
os.system(f'{cmd}')


geo = scorpy.ExpGeom(f'{geompath}')

# plt.figure()
# geo.plot_panels()
# geo.plot_qring(qmax, ec='white')
# ax = plt.gca()
# ax.set_facecolor("black")
# plt.show()



pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo)

pk.plot_peaks(cmap='spring')
ax = plt.gca()
ax.set_facecolor("black")
pk.geo.plot_qring(qmax, ec='white')



# qs = [0.0885,0.1280, 0.1545, 0.1785, 0.2020, 0.2205, 0.2550]

# qs2 = [0.0857, 0.0937, 0.1227, 0.1307, 0.1517,0.1597,0.1757,0.1835,0.1967,0.2047,0.2152,0.2230,0.2495,0.2575]

# for q in qs:
    # pk.geo.plot_qring(q, ec='red')
# # for q in qs2:
    # # pk.geo.plot_qring(q, ec='blue')

# # corrpts = scorpy.CorrelationVol(qmax=0.264).qpts



# print(pk.scat_rect)
# pk_int = pk.integrate_peaks(integration_r)
# print(pk_int.scat_rect)

# pk_int.plot_peaks(cmap='spring')
# ax = plt.gca()
# ax.set_facecolor("black")
# # pk.geo.plot_qring(qmax, ec='white')
# pk_int.geo.plot_qring(scorpy.utils.convert_r2q(integration_r, pk.geo.clen, pk.geo.wavelength), ec='green')

# for q in qs:
    # pk.geo.plot_qring(q, ec='red')
# for q in qs2:
    # pk.geo.plot_qring(q, ec='blue')

# for q in qs:
    # pk.geo.plot_qring(q, ec='red')

# for q in corrpts[::4]:
    # pk.geo.plot_qring(q, ec='blue')

# for q in corrpts[::2]:
    # pk.geo.plot_qring(q, ec='purple')


plt.show()

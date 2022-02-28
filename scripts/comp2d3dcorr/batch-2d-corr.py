




import os
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import time


## parameters
size = 75
photonenergy = 9300
qmax=0.21
qmin=0.01
clen = 0.45
npix = 250
pixsize = 800e-6
nphotons=1e24
nofringes=True

nframes = 500
nbatches = 100
geomfname = 'batch.geom'
pdbfname = 'inten1-qmax1.pdb'
intenfname = 'inten1-qmax1-sf.hkl'
method = 'scat_sph'

corrfname = 'inten1-qmax1-2d-ssph-batch50k-qcor.dbin'



corr_total = scorpy.CorrelationVol(nq=100, npsi=180, qmax=qmax, cos_sample=False, inc_self_corr=False)
# corr_total.save(f'{scorpy.DATADIR}/dbins/{corrfname}')


#write geom
geomf = open(f'{scorpy.DATADIR}/geoms/{geomfname}', 'w')
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

geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/{geomfname}')





cmd = 'pattern_sim '
cmd+='--random-orientation '
cmd+='--really-random '
cmd+='--gpu '
cmd+=f'-n {nframes} '
cmd+=f'--max-size={size} '
cmd+=f'--min-size={size} '
cmd+=f'--nphotons={nphotons} '
cmd+=f'--photon-energy={photonenergy} '
if nofringes:
    cmd+=f'--no-fringes '
cmd+=f'--intensities={scorpy.DATADIR}/xtal/{intenfname} '
cmd+=f'--spectrum=tophat '
cmd+=f'--sample-spectrum=1 '
cmd+=f'--gradients=mosaic '
cmd+=f'-g {scorpy.DATADIR}/geoms/{geomfname} '
cmd+=f'-p {scorpy.DATADIR}/xtal/{pdbfname} '

if nframes>1:
    cmd+=f'-o /tmp/corrbatch'
else:
    cmd+=f'-o /tmp/corrbatch-1.h5'




print('############')
print(f'Correlation started: {time.asctime()}\n')
for batch in range(nbatches):

    print('batch:', batch, end='\n')
    for file in os.listdir('/tmp/'):
        if 'corrbatch' in file:
            os.remove(f'/tmp/{file}')

    os.system(f'{cmd} >/dev/null 2>&1')

    for frame in range(1, nframes+1):
        print('frame:', frame, end='\r')

        pk = scorpy.PeakData(f'/tmp/corrbatch-{frame}.h5', geo=geo, qmax=qmax, qmin=qmin)
        corr_total.fill_from_peakdata(pk, method=method, verbose=0)
    print()


print(f'Correlation finished: {time.asctime()}\n')
print('############')
corr_total.save(f'{scorpy.DATADIR}/dbins/{corrfname}')


corr_total.plot_q1q2()
corr_total.plot_q1q2(log=True)
plt.show()











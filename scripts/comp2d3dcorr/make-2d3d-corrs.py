
import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import os
import time



run_3d = True
run_2d = False






######3D CORR Parameters
qmax = 1.5
ciffname = 'ortho-intenr-qmax15'
nq = 100
npsi = 180
cos_sample = False
inc_self_corr = True

corr3dfname = 'ortho-intenr-qmax15-3d-qcor.dbin'


######2D CORR Parameters
size = 75
photonenergy = 9300
clen = 0.30
npix = 1000
pixsize = 200e-6
nphotons=1e24
nofringes=True
integration_r = 0.005
pdbfname = 'ortho-intenr-qmax15-sf.pdb'
intenfname = 'ortho-intenr-qmax15-sf.hkl'
geomfname = 'batch.geom'
#approx 40 mins for 100x100, 20 mins for 50x100, 7hrs for 2000x50
nbatches = 2000
nframes = 50

method = 'scat_sph'
integrated = True

corr2dfname = 'ortho-intenr-qmax15-2d-qcor.dbin'






######3D CORR

if run_3d:
    cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{ciffname}', qmax=qmax)
    corr3d = scorpy.CorrelationVol(qmax=qmax, nq=nq, npsi=npsi, cos_sample=cos_sample, inc_self_corr=inc_self_corr)
    corr3d.fill_from_cif(cif, verbose=2, method='scat_sph')
    corr3d.save(f'{scorpy.DATADIR}/dbins/{corr3dfname}')









######2D CORR

if run_2d:

    corr2d = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=cos_sample, inc_self_corr=inc_self_corr)


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
    cmd+='--gpu '
    cmd+=f'-n {nframes} '
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

    if nframes>1:
        cmd+=f'-o /tmp/corrbatch '
    else:
        cmd+=f'-o /tmp/corrbatch-1.h5 '

    cmd+='--random-orientation '
    cmd+='--really-random '





    print('############')
    print(f'Correlation started: {time.asctime()}\n')
    for batch in range(nbatches):


        print('batch:', batch+1, end='\r')
        for file in os.listdir('/tmp/'):
            if 'corrbatch' in file:
                os.remove(f'/tmp/{file}')

        os.system(f'{cmd} >/tmp/corrbatch-patternsim.log 2>&1')

        for frame in range(1, nframes+1):


            pk = scorpy.PeakData(f'/tmp/corrbatch-{frame}.h5', geo=geo, qmax=qmax)
            if integrated:
                pk = pk.integrate_peaks(integration_r)
            corr2d.fill_from_peakdata(pk, method=method, verbose=0)


        if batch % 50==0:
            corr2d.save(f'{scorpy.DATADIR}/dbins/{corr2dfname}-batch{batch}.dbin')

        corr2d.save(f'{scorpy.DATADIR}/dbins/{corr2dfname}')


    print(f'Correlation finished: {time.asctime()}\n')
    print('############')
    corr2d.save(f'{scorpy.DATADIR}/dbins/{corr2dfname}')









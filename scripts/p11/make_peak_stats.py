import numpy as np
import matplotlib.pyplot as plt
import scorpy
import glob




datapath = f'/home/ec2-user/corr/data/p11'


runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# runs = [i for i in range( 11, 25 )] 
# runs = [i for i in range(40, 61) ]

# runs = [ 13] 

for run in runs:
    print(f'Starting run:\t{run}')
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    npklists = len(glob.glob(f'{runpath}/pklists/pklist-*.npy'))

    maxintens = np.zeros(npklists)
    numpeaks = np.zeros(npklists)
    for i in range(npklists):
        print(i, end='\r')
        pkfname = f'{runpath}/pklists/pklist-{i}.npy'
        pk = scorpy.PeakData(pkfname, f'{datapath}/crystfel_calc/eiger.geom')

        numpeaks[i] = pk.scat_qpol.shape[0]
        if pk.scat_qpol.shape[0] > 0:
            maxintens[i] = np.max(pk.scat_qpol[:,-1])


    np.save(f'{runpath}/pklists/run{run}_maxintens', maxintens)
    np.save(f'{runpath}/pklists/run{run}_numpeaks', numpeaks)





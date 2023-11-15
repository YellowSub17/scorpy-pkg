import numpy as np
import matplotlib.pyplot as plt
import scorpy
import glob




datapath = f'/home/ec2-user/corr/data/p11'


runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
runs = [i for i in range( 11, 25 )] 
runs = [i for i in range(40, 61) ]

# for run in runs:
    # print(f'Starting run:\t{run}')
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    # pklists = glob.glob(f'{runpath}/pklists/pklist-*.npy')

    # numpeaks = np.zeros(len(pklists))
    # for i, pklist in enumerate(pklists):
        # print(i, end='\r')
        # pk = scorpy.PeakData(pklist, f'{datapath}/crystfel_calc/eiger.geom')
        # numpeaks[i] = pk.scat_qpol.shape[0]
    # np.save(f'{runpath}/pklists/run{run}_numpeaks', numpeaks)




runs = [56]
for run in runs:
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    numpeaks = np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')


    counts, bins = np.histogram(numpeaks, bins=1000)

    plt.figure()

    plt.hist(bins[:-1], bins, weights=np.log10(counts +1))

plt.show()


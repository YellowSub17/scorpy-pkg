import numpy as np
import matplotlib.pyplot as plt
import scorpy
import glob

plt.rc('font', size=8)




datapath = f'/home/ec2-user/corr/data/p11'


# runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# runs = [i for i in range( 11, 25 )] 
# runs = [i for i in range(40, 61) ]



runs_opt = 'all'
runs_opt = 13







if runs_opt ==  'all':
    runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
else:
    runs = [ runs_opt ]



for i_run, run in enumerate( runs):
    print(run)
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'


    crystals = np.load(f'{runpath}/unitcells.npy')

    da = crystals[:,2]*10




plt.figure(figsize=(8/2.54, 8/2.54), dpi = 300)


counts, bins = np.histogram(da, bins = 100, density=True)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0,0,0), label=f'{runs_opt}')

plt.xlabel('a')
plt.ylabel('Frequency')


plt.legend(title=f'Run: {runs_opt}')

plt.tight_layout()




plt.show()

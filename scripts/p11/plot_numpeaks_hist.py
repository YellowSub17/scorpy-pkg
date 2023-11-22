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
runs_opt = 56







if runs_opt ==  'all':
    runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
else:
    runs = [ runs_opt ]

all_numpeaks = []
all_maxintens = []


for i_run, run in enumerate( runs):
    print(run)
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'


    numpeaks =np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')
    maxintens =np.load(f'{runpath}/pklists/run{run}_maxintens.npy')
    all_numpeaks +=list(numpeaks)
    all_maxintens +=list(maxintens)





all_maxintens = np.array(all_maxintens)
all_numpeaks = np.array(all_numpeaks)


all_maxintens_val = 1e4
binwidth = 1

loc = np.where(np.logical_and(all_numpeaks>1, all_maxintens<all_maxintens_val))
grp_ab = all_numpeaks
grp_ab_loc = all_numpeaks[loc]
grp_a_loc = all_numpeaks[loc][::2]
grp_b_loc = all_numpeaks[loc][1::2]


plt.figure(figsize=(8/2.54, 8/2.54), dpi = 300)


bins = np.arange(0, np.max(grp_ab)+binwidth, binwidth)
counts,_= np.histogram(grp_ab, bins=bins)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0,0,0), label='All')

counts,_= np.histogram(grp_ab_loc, bins=bins)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0, 1, 1, 0.75), label='Crop')

plt.xlabel('Number of Peaks in a Frame')
plt.ylabel('Frequency')


plt.legend(title=f'Run: {runs_opt}')

plt.tight_layout()




plt.figure(figsize=(8/2.54, 8/2.54), dpi = 300)


bins = np.arange(0, np.max(grp_ab_loc)+binwidth, binwidth)
counts,_= np.histogram(grp_a_loc, bins=bins)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0,0,1,1), label='Half a')
counts,_= np.histogram(grp_b_loc, bins=bins)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(1, 0, 0,0.75 ), label='Half b')


plt.xlabel('Number of Peaks in a Frame')
plt.ylabel('Frequency')
plt.legend(title=f'Run: {runs_opt}')

plt.tight_layout()


plt.show()

